# IssueActions.py
from datetime import datetime, timezone
import google.generativeai as genai

from DatabaseManager import DatabaseManager
from secret import GEMINI_API_KEY # Dodaj ten import!

class IssueActions:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.create_table()
        self.allowed_statuses = {"new", "reviewed", ""} 

        genai.configure(api_key=GEMINI_API_KEY)
        
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')

    def summarize_issues(self):
        issues = self.fetch_issues('new')
        if isinstance(issues, str): 
            return f"Błąd podczas pobierania zgłoszeń do podsumowania"
        if not issues:
            return "Brak nowych zgłoszeń do podsumowania."

        # full_text = "\n".join(f"<issue>Zgłoszenie {issue[0]} - {issue[1]}: {issue[2]}</issue>" for issue in issues)
        formatted_issues_list = [
            f"<issue>Zgłoszenie {issue[0]} - {issue[1]}: {issue[2]}</issue>"
            for issue in issues
        ]
        full_text = "\n".join(formatted_issues_list)

        try:
            prompt = (
                f"Poniżej znajduje się lista zgłoszeń. Pogrupuj je według pilności w rankingu top 5. Domyślnie wyższe pozycje są pilniejsze.\n"
                f"Dla każdego zgłoszenia, wymień jego ID, Tytuł i krótki opis problemu.\n"
                f"\nOto zgłoszenia:\n{full_text}\n\n"
                f"Podział według pilności:"
            )
            
            response = self.gemini_model.generate_content(prompt)
            
            summary = response.text
            return "\n" + summary
        except Exception as e:
            return f"Wystąpił błąd podczas generowania podsumowania za pomocą Gemini API: {e}"

    def insert_issue(self, title, description, date_created=datetime.now(timezone.utc)):
        error_message = ""
        if not isinstance(title, str) or not title.strip():
            error_message += "\nBłąd: Tytuł musi być niepustym tekstem."
        if not isinstance(description, str) or not description.strip(): 
            error_message += "\nBłąd: Opis musi być niepustym tekstem."
        
        if len(error_message) > 0:
            return error_message
        else:
            date_created_str = date_created.strftime("%Y-%m-%d %H:%M:%S")
            return self.db.insert_issue(title, description, date_created_str)

    def delete_issue(self, issue_id):
        try:
            issue_id = int(issue_id)
            if issue_id < 0: return "Issue ID musi być nieujemną liczbą całkowitą." 
        except ValueError:
            return "Issue ID musi być nieujemną liczbą całkowitą." 
        
        return self.db.delete_issue(issue_id)

    def update_status(self, issue_id, status="reviewed"):
        error_message = ""
        try:
            issue_id = int(issue_id)
            if issue_id < 0: error_message += "Issue ID musi być nieujemną liczbą całkowitą.\n"
        except ValueError: 
            error_message += "Issue ID musi być nieujemną liczbą całkowitą.\n"

        if status == "":
            status = "reviewed" 

        if status not in self.allowed_statuses:
            error_message += f"Status musi być jednym z: {', '.join(s for s in self.allowed_statuses if s != '')} (puste oznacza 'reviewed')."

        if len(error_message) > 0:
            return error_message
        
        return self.db.update_status(issue_id, status)

    def fetch_issues(self, status=None):
        if status == "":
            status_to_fetch = None
        elif status is not None and status not in self.allowed_statuses:
             return f"Status musi być jednym z: {', '.join(s for s in self.allowed_statuses if s != '')} lub pusty, aby wyświetlić wszystkie."
        else:
            status_to_fetch = status

        return self.db.fetch_issues(status_to_fetch)