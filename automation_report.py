from app import app,send_pending_task_reminders

if __name__ == "__main__":
    with app.app_context():
        count = send_pending_task_reminders()
        print(f"Done. Reminders sent to {count} user(s).")