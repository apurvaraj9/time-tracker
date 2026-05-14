# Dictionary of categories and their keywords.
# Add your own keywords here anytime!
CATEGORIES = {
    "Coding": [
        "visual studio code", "vscode", "pycharm", "sublime",
        "github", "stack overflow", "terminal", "cmd",
        "jupyter", "git", "python", "intellij", "eclipse"
    ],
    "Browsing": [
        "google", "bing", "yahoo", "new tab",
        "mozilla firefox", "microsoft edge"
    ],
    "Entertainment": [
        "youtube", "netflix", "prime video", "hotstar",
        "spotify", "vlc", "twitch", "instagram", "facebook", "brave"
    ],
    "Communication": [
        "whatsapp", "telegram", "gmail", "outlook",
        "thunderbird", "discord", "slack", "messenger"
    ],
    "Meeting": [
        "zoom", "google meet", "teams", "webex",
        "skype", "bluejeans"
    ],
    "Documents": [
        "word", "excel", "powerpoint", "notepad",
        "google docs", "google sheets", "pdf", "notion"
    ],
    "System": [
        "task manager", "control panel", "settings",
        "file explorer", "this pc"
    ],
}

def categorize(window_title):
    """
    Takes a window title string and returns its category.
    Returns 'Uncategorized' if no keyword matches.
    """
    # Convert to lowercase so matching is not case-sensitive
    title_lower = window_title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    # Nothing matched
    return "Uncategorized"