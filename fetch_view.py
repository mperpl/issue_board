from IssueActions import IssueActions
while True:
    actions = IssueActions()
    status = input('===================================================\n\nWyświetl zgłoszenia:\n\n \
    ENTER by wyświetlić wszystkie\n \
    "new", "reviewed" by wyświetlić według statusu\n\n \
    wejście: ')
    issues = actions.fetch_issues(status)
    for i in issues:
        print(f"""\

    | id: {i[0]}
    | issue: {i[1]}
    | describtion: {i[2]}
    | status: {i[3]}
    | date created: {i[4][:16]}

        """)