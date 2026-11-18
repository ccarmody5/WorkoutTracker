"""User-facing Workout Tracker release history, newest first."""

REVISIONS = [
    {
        'version': '1.1.1',
        'date': '2026-11-18',
        'title': 'Manage Activities navigation fix',
        'changes': [
            'The Manage Activities button opens the activity editor without inline JavaScript.',
            'Restart the application to load this update.',
        ],
    },
    {
        'version': '1.1.0',
        'date': '2026-11-18',
        'title': 'Manage workout activities',
        'changes': [
            'Use Manage Activities in the home menu to add, rename, enable, or disable activities.',
            'Restart the application to load this update.',
        ],
    },
    {
        'version': '1.0.1',
        'date': '2026-11-18',
        'title': 'Version in the page header',
        'changes': [
            'The application version appears below the title on the home and user selection pages.',
            'Restart the application to load this update.',
        ],
    },
    {
        'version': '1.0.0',
        'date': '2026-11-18',
        'title': 'Application version and release history',
        'changes': [
            'The home and user selection pages show the current application version.',
            'The About page lists the latest release and any previous releases.',
            'Restart the application to load this update.',
        ],
    },
]

APP_REVISION = REVISIONS[0]['version']
