import sqlite3

class DatabaseManager:
    ######################
    ##### TABLE PART #####
    #############################################
    def __init__(self, db_name="issue_board.db"):
        self.db_name = db_name

    ############################
    def create_connection(self):
        return sqlite3.connect(self.db_name)


    #####################################
    def create_table(self, sample=False):
        conn = self.create_connection()
        cursor = conn.cursor()
        # ISSUE TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            date_created TIMESTAMP NOT NULL
        );
        """)

        if sample is True:
            sample_issues = [
                ("Brak Internetu", "W sali 101 od rana nie ma połączenia z siecią Wi-Fi. Użytkownicy nie mogą korzystać z internetu, co blokuje dostęp do zasobów online i systemów firmowych. Sieć była restartowana, ale problem nadal występuje. Konieczne jest pilne rozwiązanie.", "new", "2025-06-22 08:15"),
                ("Błąd w aplikacji", "Po kliknięciu przycisku 'Zatwierdź' aplikacja natychmiast się zawiesza. Problem pojawił się po ostatniej aktualizacji i uniemożliwia dalszą pracę z dokumentami. Zespół programistów prowadzi już prace nad naprawą błędu.", "reviewed", "2025-06-21 13:42"),
                ("Zamknięte drzwi", "Drzwi do serwerowni są zamknięte i nikt nie ma obecnie dostępu. Brak klucza lub kodu blokuje możliwość przeprowadzenia niezbędnej konserwacji sprzętu. Sytuacja wymaga pilnej interwencji administracji budynku.", "reviewed", "2025-06-20 09:00"),
                ("Uszkodzony projektor", "Projektor w sali 204 wyświetla tylko zielony obraz, niezależnie od podłączonego urządzenia. Sprzęt jest wykorzystywany podczas prezentacji i szkoleń, co powoduje opóźnienia w harmonogramie. Potrzebna szybka diagnoza i naprawa lub wymiana urządzenia.", "new", "2025-06-22 10:05"),
                ("Problem z logowaniem", "Użytkownicy zgłaszają, że nie mogą się zalogować do systemu ERP. System wyświetla komunikaty o błędach autoryzacji i odrzuca próby logowania. Problem występuje od dwóch dni i dotyczy większości pracowników.", "new", "2025-06-18 16:25"),
                ("Awaria klimatyzacji", "Temperatura w sali 301 przekracza 30 stopni Celsjusza, ponieważ klimatyzacja nie działa. Wysoka temperatura powoduje dyskomfort pracowników i obniża efektywność pracy. Konserwacja urządzenia jest pilnie potrzebna.", "reviewed", "2025-06-21 14:55"),
                ("Zgubiony pendrive", "W sali 105 znaleziono nieoznaczony pendrive. Nie wiadomo, do kogo należy i jakie dane zawiera. Pendrive został zabezpieczony i przekazany do działu IT w celu analizy bezpieczeństwa.", "reviewed", "2025-06-20 11:11"),
                ("Nowy pomysł na aplikację", "Zaproponowano dodanie widoku kalendarza do aplikacji służącej do organizacji zadań. Funkcja ta miałaby usprawnić planowanie i koordynację pracy zespołu. Pomysł czeka na ocenę i możliwą implementację w przyszłych wersjach.", "reviewed", "2025-06-22 07:50"),
                ("Błąd synchronizacji", "Dane nie synchronizują się poprawnie między klientem a serwerem. Część informacji jest tracona lub pojawia się z opóźnieniem, co negatywnie wpływa na spójność bazy danych. Zespół techniczny prowadzi już analizę problemu.", "new", "2025-06-22 08:30"),
                ("Sprzęt testowy", "Nowe urządzenie testowe zostało dostarczone do laboratorium IT. Konfiguracja i testy kompatybilności z istniejącym systemem muszą zostać przeprowadzone pilnie. Sprzęt jest potrzebny do realizacji kluczowych badań i projektów.", "reviewed", "2025-06-21 10:10"),
                ("Problemy z drukarką", "Drukarka sieciowa w biurze głównym regularnie się zacina i nie drukuje niektórych dokumentów. Użytkownicy skarżą się na błędy podczas drukowania raportów. Potrzebna jest wymiana lub naprawa urządzenia.", "new", "2025-06-22 09:20"),
                ("Opóźnienie aktualizacji systemu", "Planowana aktualizacja oprogramowania została opóźniona z powodu błędów wykrytych podczas testów. Opóźnienie wpływa na harmonogram wdrożeń i rozwój nowych funkcji.", "reviewed", "2025-06-21 16:40"),
                ("Brak dostępu do baz danych", "Niektórzy użytkownicy tracą dostęp do kluczowych baz danych, co utrudnia im realizację zadań. Problem pojawił się po zmianach w konfiguracji sieci.", "new", "2025-06-22 11:00"),
                ("Problemy z backupem", "Automatyczne kopie zapasowe nie są tworzone zgodnie z harmonogramem. Brak aktualnych backupów stwarza ryzyko utraty danych w przypadku awarii.", "new", "2025-06-22 07:30"),
                ("Awaria zasilania serwera", "Serwer główny został wyłączony z powodu awarii zasilania. Trwają prace nad przywróceniem zasilania i uruchomieniem systemu.", "reviewed", "2025-06-21 22:15"),
                ("Niska wydajność aplikacji", "Użytkownicy zgłaszają, że aplikacja działa bardzo wolno, zwłaszcza podczas generowania raportów. Wydajność jest na poziomie zagrażającym terminowości pracy.", "reviewed", "2025-06-20 12:30"),
                ("Problem z kamerą monitoringu", "Kamera monitoringu w holu głównym przestała przesyłać obraz. Konieczna jest szybka naprawa w celu zapewnienia bezpieczeństwa.", "new", "2025-06-22 06:50"),
                ("Błąd w module raportowania", "Raporty generowane przez moduł finansowy zawierają nieprawidłowe dane. Problem wymaga natychmiastowej korekty, aby uniknąć błędnych decyzji biznesowych.", "reviewed", "2025-06-21 15:00"),
                ("Nieaktualne oprogramowanie", "Na kilku stanowiskach zainstalowane jest nieaktualne oprogramowanie, co stwarza ryzyko bezpieczeństwa. Potrzebna jest aktualizacja i standaryzacja wersji.", "reviewed", "2025-06-20 09:45"),
                ("Problemy z VPN", "Użytkownicy pracujący zdalnie zgłaszają częste rozłączenia z VPN, co utrudnia dostęp do zasobów firmowych.", "new", "2025-06-22 08:05"),
                ("Uszkodzony ekran monitora", "Ekran monitora w sali konferencyjnej 3 ma pęknięcia i przebarwienia, co utrudnia korzystanie podczas spotkań.", "new", "2025-06-22 09:55"),
                ("Brak tonera w drukarce", "W drukarce w dziale kadr skończył się toner, co powoduje przerwy w drukowaniu dokumentów kadrowych.", "new", "2025-06-18 11:30"),
                ("Problemy z pocztą elektroniczną", "Poczta elektroniczna często nie dostarcza wiadomości do niektórych odbiorców lub opóźnia ich dostarczenie.", "reviewed", "2025-06-21 14:20"),
                ("Nieprawidłowa konfiguracja sieci", "Konfiguracja routera głównego została zmieniona bez zgody działu IT, co powoduje problemy z połączeniem dla części użytkowników.", "reviewed", "2025-06-20 10:10"),
                ("Awaria oprogramowania księgowego", "Oprogramowanie księgowe przestało działać prawidłowo po ostatniej aktualizacji. Brak możliwości wprowadzania danych finansowych.", "new", "2025-06-22 07:40"),
                ("Niewystarczająca liczba stanowisk pracy", "Z powodu wzrostu liczby pracowników brakuje stanowisk z odpowiednim wyposażeniem. Konieczne jest rozbudowanie infrastruktury IT.", "reviewed", "2025-06-21 09:25"),
                ("Problemy z systemem rezerwacji sal", "System rezerwacji sal konferencyjnych nie zapisuje poprawnie nowych rezerwacji, co prowadzi do konfliktów terminów.", "reviewed", "2025-06-21 11:50"),
            ]
            cursor.executemany("INSERT OR IGNORE INTO issues (id, title, description, status, date_created) VALUES (NULL ,?, ?, ?, ?)", sample_issues)

        conn.commit()
        conn.close()


    #######################
    ##### ISSUES PART #####
    #########################################################
    def insert_issue(self, title, description, date_created):
        conn = self.create_connection()
        cursor = conn.cursor()

        issue = (title, description, date_created)

        cursor.execute("INSERT OR IGNORE INTO issues (id, title, description, status, date_created) VALUES (NULL, ?, ?, 'new', ?)", issue)

        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return "Insertion ignored."
        else:
            return "Issue committed."



    #################################
    def delete_issue(self, issue_id):
        conn = self.create_connection()
        cursor = conn.cursor()

        cursor.execute(f"DELETE FROM issues WHERE id=?", (issue_id,))
        affected = cursor.rowcount

        conn.commit()
        conn.close()

        if affected > 0:
            return f"Issue {issue_id} deleted."
        else:
            return f"No issue found with id {issue_id}."


    ##########################################
    def update_status(self, issue_id, status):
        conn = self.create_connection()
        cursor = conn.cursor()

        cursor.execute(f"UPDATE issues SET status=? WHERE id=?", (status, issue_id))
        affected = cursor.rowcount

        conn.commit()
        conn.close()
        
        if affected > 0:
            return f"Issue {issue_id} updated."
        else:
            return f"No issue found with id {issue_id}."



    ###############################
    def fetch_issues(self, status):
        conn = self.create_connection()
        cursor = conn.cursor()

        if status:
            cursor.execute("SELECT * FROM issues WHERE status=? ORDER BY date_created DESC", (status,))
        else:
            cursor.execute("SELECT * FROM issues ORDER BY date_created DESC")

        rows = cursor.fetchall()

        conn.close()

        print("Issues fetched.")
        return rows