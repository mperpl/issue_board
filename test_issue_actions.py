# python -m unittest test_issue_actions.py
import unittest
import sqlite3
import os
import time
import google.generativeai as genai
from datetime import datetime, timezone

# --- Mocks dla zewnętrznych zależności ---
class MockGenerativeModel:
    """Mokuje model Google Gemini API, aby uniknąć rzeczywistych wywołań API podczas testów."""
    def generate_content(self, prompt):
        expected_summary = "- **ID:** 1\n- **Tytuł:** Test Pilny Problem\n- **Problem:** Kluczowy błąd wymagający natychmiastowej uwagi."
        return MockResponse(expected_summary)

class MockResponse:
    """Prosty mock dla obiektu odpowiedzi API, zawierający atrybut 'text'."""
    def __init__(self, text):
        self.text = text

# --- Definicje klas testowych ---
from DatabaseManager import DatabaseManager
from IssueActions import IssueActions

class TestIssueActions(unittest.TestCase):

    def setUp(self):
        """Ustawia świeżą, tymczasową bazę danych dla każdego testu."""
        self.test_db_name = "test_issue_board.db"

        if os.path.exists(self.test_db_name):
            try:
                temp_conn = sqlite3.connect(self.test_db_name)
                temp_conn.close()
                os.remove(self.test_db_name)
            except (sqlite3.Error, PermissionError) as e:
                print(f"Ostrzeżenie w setUp: Nie można usunąć starej bazy testowej '{self.test_db_name}': {e}")
                pass
        
        self.db_manager = DatabaseManager(self.test_db_name)
        self.db_manager.create_table(sample=False) 

        self.actions = IssueActions()
        self.actions.db = self.db_manager 
        
        self.actions.gemini_model = MockGenerativeModel()

        genai.configure(api_key="TEST_API_KEY_MOCK") 

    def tearDown(self):
        """Czyści środowisko po każdym teście, usuwając plik testowej bazy danych."""
        if os.path.exists(self.test_db_name):
            try:
                os.remove(self.test_db_name)
            except PermissionError as e:
                print(f"Ostrzeżenie w tearDown: Nie można usunąć '{self.test_db_name}'. Może być nadal używany: {e}")
                pass

    # --- Metody testowe ---

    def test_insert_issue(self):
        """Testuje, czy zgłoszenie może być pomyślnie wstawione do bazy danych."""
        now_dt = datetime.now(timezone.utc) 
        result = self.actions.insert_issue("Testowy tytuł", "Testowy opis", now_dt)
        self.assertIn(result, ["Issue committed.", "Insertion ignored."]) 
        
        issues = self.actions.fetch_issues(None)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0][1], "Testowy tytuł")

    def test_insert_issue_empty_title(self):
        """Testuje walidację dla wstawiania zgłoszenia z pustym tytułem."""
        now_dt = datetime.now(timezone.utc)
        result = self.actions.insert_issue("", "Testowy opis", now_dt)
        self.assertIn("Błąd: Tytuł musi być niepustym tekstem.", result)

    def test_insert_issue_empty_description(self):
        """Testuje walidację dla wstawiania zgłoszenia z pustym opisem."""
        now_dt = datetime.now(timezone.utc)
        result = self.actions.insert_issue("Test title", "", now_dt)
        self.assertIn("Błąd: Opis musi być niepustym tekstem.", result)

    def test_update_status(self):
        """Testuje, czy status istniejącego zgłoszenia może zostać zaktualizowany."""
        now_dt = datetime.now(timezone.utc)
        self.actions.insert_issue("Test do aktualizacji", "Opis do aktualizacji", now_dt)
        
        issues = self.actions.fetch_issues(None)
        self.assertGreater(len(issues), 0, "Warunek wstępny: Co najmniej jedno zgłoszenie powinno istnieć dla testu aktualizacji.")
        issue_id = issues[0][0]

        result = self.actions.update_status(issue_id, "reviewed")
        self.assertIn(f"Issue {issue_id} updated.", result) 
        
        updated_issues = self.actions.fetch_issues("reviewed")
        self.assertEqual(len(updated_issues), 1)
        self.assertEqual(updated_issues[0][3], "reviewed")

    def test_update_status_invalid_id(self):
        """Testuje walidację dla aktualizacji statusu z nieprawidłowym (niecałkowitym) ID."""
        result = self.actions.update_status("abc", "reviewed")
        self.assertIn("Issue ID musi być nieujemną liczbą całkowitą.", result)

    def test_update_status_negative_id(self):
        """Testuje walidację dla aktualizacji statusu z ujemnym ID."""
        result = self.actions.update_status(-5, "reviewed")
        self.assertIn("Issue ID musi być nieujemną liczbą całkowitą.", result)

    def test_update_status_invalid_status(self):
        """Testuje walidację dla aktualizacji statusu z nieautoryzowanym ciągiem statusu."""
        now_dt = datetime.now(timezone.utc)
        self.actions.insert_issue("Test statusu", "Opis statusu", now_dt)
        
        issues = self.actions.fetch_issues(None)
        self.assertGreater(len(issues), 0, "Warunek wstępny: Co najmniej jedno zgłoszenie powinno istnieć dla testu statusu.")
        issue_id = issues[0][0]

        result = self.actions.update_status(issue_id, "invalid_status")
        self.assertIn("Status musi być jednym z:", result)

    def test_summarize_issues(self):
        """Testuje funkcjonalność podsumowywania AI za pomocą mock modelu."""
        now_dt = datetime.now(timezone.utc)
        self.actions.insert_issue("Pilny błąd systemu produkcyjnego", "System nie działa, blokuje kluczowe operacje dla wielu użytkowników.", now_dt)
        self.actions.insert_issue("Mały błąd wizualny na stronie", "Ikona jest trochę przesunięta, ale funkcjonalność jest zachowana.", now_dt)
        self.actions.insert_issue("Utrata danych klienta", "Potencjalna utrata danych osobowych dla 500 klientów, pilne do naprawy.", now_dt)
        
        summary = self.actions.summarize_issues()
        # This assertion MUST EXACTLY match the string returned by MockGenerativeModel above.
        self.assertIn("- **ID:** 1\n- **Tytuł:** Test Pilny Problem\n- **Problem:** Kluczowy błąd wymagający natychmiastowej uwagi.", summary) 
        self.assertIsInstance(summary, str) 
        self.assertGreater(len(summary), 50) 

    def test_summarize_issues_no_new_issues(self):
        """Testuje podsumowanie AI, gdy nie ma nowych zgłoszeń."""
        summary = self.actions.summarize_issues()
        self.assertEqual("Brak nowych zgłoszeń do podsumowania.", summary)


    def test_delete_issue(self):
        """Testuje, czy zgłoszenie może być pomyślnie usunięte."""
        now_dt = datetime.now(timezone.utc)
        self.actions.insert_issue("Zgłoszenie do usunięcia", "Opis do usunięcia testowego.", now_dt)
        
        issues_before_delete = self.actions.fetch_issues(None)
        self.assertEqual(len(issues_before_delete), 1, "Warunek wstępny: Jedno zgłoszenie powinno istnieć przed usunięciem.")
        issue_id = issues_before_delete[0][0]
        
        result = self.actions.delete_issue(issue_id)
        self.assertIn(f"Issue {issue_id} deleted.", result) 
        
        remaining_issues = self.actions.fetch_issues(None)
        self.assertEqual(len(remaining_issues), 0)

    def test_delete_issue_invalid_id(self):
        """Testuje walidację dla usuwania zgłoszenia z nieprawidłowym (niecałkowitym) ID."""
        result = self.actions.delete_issue("xyz")
        self.assertIn("Issue ID musi być nieujemną liczbą całkowitą.", result)
        
    def test_delete_issue_non_existent(self):
        """Testuje usuwanie nieistniejącego zgłoszenia."""
        result = self.actions.delete_issue(9999) 
        self.assertIn("No issue found with id 9999.", result) 


if __name__ == '__main__':
    unittest.main()