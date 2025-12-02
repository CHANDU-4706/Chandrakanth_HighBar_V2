# Run these commands one by one in your PowerShell terminal

# 1. Go to the correct folder
cd "c:\Users\CHANDU\OneDrive\Desktop\Project\Chandrakanth_HighBar_V2"

# 2. Configure your Git Identity (Replace with your details)
git config user.email "chandu@example.com"
git config user.name "Chandrakanth"

# 3. Point to your NEW GitHub repository
# Make sure you have created 'Chandrakanth_HighBar_V2' on GitHub first!
git remote set-url origin https://github.com/CHANDU-4706/Chandrakanth_HighBar_V2.git

# 4. Push your code
git add .
git commit -m "V2 High Bar Submission"
git push -u origin main
