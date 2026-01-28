from modules.security_hardening import SecurityHardener

try:
    hardener = SecurityHardener()
    print("Checking OS...")
    if not hardener.check_os():
        print("Not Windows. Skipping.")
    else:
        print("Running Posture Checks...")
        results = hardener.check_posture()
        for check, (curr, rec, fix) in results.items():
            status = "FAIL" if fix else "PASS"
            print(f"[{status}] {check}: Current={curr}, Rec={rec}, NeedsFix={fix}")

except Exception as e:
    print(f"Test Failed with Error: {e}")
