from IssueActions import IssueActions
import subprocess

actions = IssueActions()

def show_menu():
    print("\n\t=== ISSUE BOARD ===")
    print("1. AI lista 5 najistotniejszych zgłoszeń")
    print("2. Dodaj zgłoszenie")
    print("3. Wyświetl zgłoszenia")
    print("4. Zmień status zgłoszenia")
    print("5. Usuń zgłoszenie")
    print("0. Wyjście")

def run():
    while True:
        show_menu()
        choice = input("Wybierz opcję: ")

        if choice == "1":
            print(actions.summarize_issues())

        elif choice == "2":
            title = input("Tytuł: ")
            desc = input("Opis: ")
            print(actions.insert_issue(title, desc))

        elif choice == "3":
            subprocess.call('taskkill /F /FI "WINDOWTITLE eq fetch_view"', shell=True)
            subprocess.Popen('start "fetch_view" cmd /k python fetch_view.py', shell=True)
            print('Otwarto widok na zgłoszenia w nowym oknie.')

        elif choice == "4":
            issue_id = input("ID zgłoszenia: ")
            new_status = input("Nowy status: ")
            print(actions.update_status(issue_id, new_status))

        elif choice == "5":
            issue_id = input("ID do usunięcia: ")
            print(actions.delete_issue(issue_id))

        elif choice == "0":
            print("Zamykam...")
            break
        else:
            print("Nieznana opcja")
