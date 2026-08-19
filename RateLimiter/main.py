
from RateLimiterService import RateLimiterService
from UserTier import UserTier


FREE = UserTier("FREE", request_limit=5, time_window=10)
PREMIUM = UserTier("PREMIUM", request_limit=10, time_window=10)


def print_menu():
    print("\nRate Limiter CLI")
    print("1. Add user")
    print("2. Login")
    print("3. Send request (logged in user)")
    print("4. Get user")
    print("5. Change user tier")
    print("6. Remove user")
    print("7. Logout")
    print("8. Exit")


def choose_tier():
    while True:
        tier_choice = input("Select tier (FREE/PREMIUM): ").strip().upper()

        if tier_choice == "FREE":
            return FREE

        if tier_choice == "PREMIUM":
            return PREMIUM

        print("Invalid tier. Please choose FREE or PREMIUM.")


def main():
    service = RateLimiterService()
    logged_in_user_id = None

    while True:
        print_menu()

        if logged_in_user_id:
            print(f"Logged in user_id={logged_in_user_id}")
        else:
            print("Logged in user_id=None")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Enter user name: ").strip()

            if not name:
                print("Name cannot be empty.")
                continue

            tier = choose_tier()
            user_id = service.add_user(name, tier, rate_limiter_type="FIXED_WINDOW")
            print(f"User created. user_id={user_id}")

        elif choice == "2":
            user_id = input("Enter user_id to login: ").strip()
            user = service.get_user(user_id)

            if user == "user not found":
                print("user not found")
            else:
                logged_in_user_id = user_id
                print(f"Login successful. Welcome {user.name}.")

        elif choice == "3":
            if not logged_in_user_id:
                print("Please login first.")
                continue

            result = service.allow_request(logged_in_user_id)

            if result == "user not found":
                logged_in_user_id = None
                print("user not found")
            elif result:
                print("Request allowed")
            else:
                print("Request blocked by fixed window limiter")

        elif choice == "4":
            user_id = input("Enter user_id: ").strip()
            user = service.get_user(user_id)

            if user == "user not found":
                print("user not found")
            else:
                print(f"name={user.name}, tier={user.tier.tier_name}")

        elif choice == "5":
            user_id = input("Enter user_id: ").strip()
            new_tier = choose_tier()
            updated = service.modify_user_tier(user_id, new_tier)

            if updated:
                print("Tier updated")
            else:
                print("user not found")

        elif choice == "6":
            user_id = input("Enter user_id: ").strip()
            removed = service.remove_user(user_id)

            if removed:
                if logged_in_user_id == user_id:
                    logged_in_user_id = None
                print("User removed")
            else:
                print("user not found")

        elif choice == "7":
            if logged_in_user_id:
                logged_in_user_id = None
                print("Logged out")
            else:
                print("No user is currently logged in")

        elif choice == "8":
            print("Exiting CLI")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
