# Workout Tracker revision management

- Read `config/app_revision.py` before editing it. Keep `REVISIONS` newest first, preserve existing entries, and use unique versions. `APP_REVISION` comes from the first entry.
- Add one entry at the beginning of `REVISIONS` per completed task that changes application behavior, UI, database schema, model handling, dependencies, or deployment behavior. Group related changes from the task into that entry.
- Use SemVer. Increment PATCH for fixes and small UI changes, MINOR for backward-compatible features, and MAJOR for incompatible changes. Reset the lower components after a MINOR or MAJOR bump.
- Each entry has `version`, `date`, `title`, and `changes`. Use the current Asia/Amman date in `YYYY-MM-DD` format and write short, user-facing notes. Include applicable migrations, restarts, and other operational requirements. Keep secrets, personal information, and raw user data out of release notes.
- Keep release-specific notes in `config/app_revision.py`. Use the Flask context variables `app_revision` and `app_revisions` for release information in templates. Keep version literals out of templates and JavaScript. Edit `templates/about.html` only when its standing content or layout needs to change.
- Documentation-only, agent-instruction-only, and test-only changes need no bump. Investigations, questions, and proposals without application changes also need no bump.
- Verify that the revision module imports and the affected templates render. Report the resulting application revision in the final response. A revision bump alone does not authorize a commit, tag, push, or deployment.
