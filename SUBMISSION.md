# GitHub upload guide — first-time beginner

## Phase 1: easiest method (no Git commands required)

1. Visit https://github.com and sign in (or create your account and verify email).
2. Visit https://github.com/new.
3. Under **Repository name**, type `skillbridge-ai`.
4. Description: `Explainable AI resume analysis, skill gaps, competency graphs and counterfactual upskilling.`
5. Select **Public**, unless your organizers explicitly require private access.
6. Do **not** check **Add a README**, `.gitignore`, or license. Click **Create repository**.
7. On the empty repository page, click **uploading an existing file** (or **Add file → Upload files**).
8. Extract the ZIP you received. Open its `skillbridge-ai` folder. Select the project files and folders **inside** it and drag them into the GitHub upload area. Do not upload the ZIP as one file. Do not upload real resumes or secrets.
9. Wait until the files are listed. Scroll down, type commit message `Add SkillBridge AI Phase 1 prototype`, then click **Commit changes**.
10. Confirm that the GitHub page shows the README, `app.py`, `engine.py`, `modules`, `assets`, `samples`, and `tests`.
11. Copy your **profile link** from your account page: `https://github.com/YOUR_USERNAME`.
12. Copy your **repository link** from your project page: `https://github.com/YOUR_USERNAME/skillbridge-ai`.
13. Open the **official FMH Google Form provided by the organizers**. Paste both links into the Phase 1 fields and submit before the extended deadline. Save the confirmation.

**Important:** Some browsers may not upload nested folders reliably by drag-and-drop. If a folder is missing, use GitHub's web editor to create the files using their paths, or use GitHub Desktop / Git CLI to push the whole directory.

## Phase 2 (only after Phase 1)

1. Run `pip install -r requirements.txt` and `streamlit run app.py` locally.
2. Fix any issues and take real screenshots.
3. Go to https://share.streamlit.io and connect GitHub.
4. Select the `skillbridge-ai` repository, branch `main`, main file `app.py`. Deploy.
5. Open the deployed URL in an incognito window and test the sample inputs.
6. Update README with the real deployed link, then submit the repository and live URL via the official Phase 2 form.

## Common mistakes

- A ZIP uploaded as one file is **not** a browsable source-code repository.
- A private repository may be inaccessible to judges.
- The GitHub profile URL and repository URL are **two different links**.
- Never publish API keys, passwords, private resumes, or invented screenshots.
- The optional semantic mode needs `requirements-semantic.txt` and an initial model download; leave it off for the fastest demo.
