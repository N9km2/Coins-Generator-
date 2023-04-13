import samino
import json
import datetime
import os
import time

def get_timezone():
    return {1: -120, 2: -180, 3: -240, 4: -300, 5: -360, 6: -420, 7: -480, 8: -540, 9: -600, 10: -660, 11: -720, 12: -780, 13: 600, 14: 540, 15: 480, 16: 420, 17: 360, 18: 300, 19: 240, 20: 180, 21: 120, 22: 60, 23: 0}[datetime.datetime.utcnow().hour]


def create_timers():
    return [{"start": int(datetime.datetime.timestamp(datetime.datetime.now())),
             "end": int(datetime.datetime.timestamp(datetime.datetime.now()))+300} for _ in range(36)]


def send_active_time(subclint, timers, timezone):
    try:
        subclint.send_active_time(timers=timers, tz=timezone)
        return True
    except Exception as e:
        print(f"Error sending request: {e}")
        return False


def login_and_send_requests(email, password, subclint):
    clint = samino.Client()
    clint.login(email=email, password=password)
    for counter in range(24):
        timers = create_timers()
        timezone = get_timezone()
        if send_active_time(subclint, timers, timezone):
            print(f"Sent request {counter+1} for {email}")
            time.sleep(2)
        else:
            break
    else:
        print(f"All requests sent for {email}")
    clint.logout()
    time.sleep(15)


def main():
    account_data = json.loads(open("accounts.json").read())
    community_link = input("Enter community link: ")
    subclint = samino.Local(comId=samino.Client().get_from_link(link=community_link))
    for account in account_data:
        try:
            login_and_send_requests(account["email"], account["password"], subclint)
        except Exception as e:
            print(f"Error for {account['email']}: {e}")
            continue
        os.system("clear")


if __name__ == '__main__':
    main()
