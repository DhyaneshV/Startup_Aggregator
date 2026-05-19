# 🛡️ Real Data & Bot Avoidance Guide

## 🔗 Link Strategy
To avoid 404 errors and improve user experience, we are now using a dual-link strategy in our JSON data:

1.  **source_link**: This is the **Main Homepage** of the organization (e.g., `https://www.nasscom.in/`). 
    - *Why?* Homepages rarely change or 404. It gives the user a place to start if the specific program page is down.
2.  **apply_link**: This is the **Specific Opportunity Page** or **Direct Apply Form**.
    - *Why?* This is where the user actually takes action.

## 🤖 Bot Avoidance (Browser vs. Script)
Many premium sites (Medium, WSJ, Bloomberg) block simple Python scripts but work fine for users.

### 🛠️ Our Solution:
- **Backend Headers**: Always use a browser-like `User-Agent` string in our scrapers and link checkers.
- **Manual Verification**: If a script returns a 403 (Forbidden), we verify it manually in a browser before flagging it as broken.
- **Graceful Failover**: If a specific `apply_link` 404s, the frontend should fall back to showing the `source_link`.

## 📝 Data Update Workflow
1.  Check links against this guide.
2.  Update `all_manual_data.json` with both `source_link` and `apply_link`.
3.  Re-run `upload_manual_data.py` to sync changes to MongoDB Atlas.

*Last Updated: May 17, 2026*
