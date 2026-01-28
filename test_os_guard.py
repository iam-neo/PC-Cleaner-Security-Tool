from utils.system_info import ensure_windows_os
import platform

print(f"Current OS: {platform.system()}")
try:
    is_win = ensure_windows_os(raise_exception=True)
    print(f"Check Result (raise=True): {is_win}")
except OSError as e:
    print(f"Check Result (raise=True): Caught Expected Error: {e}")

is_win_safe = ensure_windows_os(raise_exception=False)
print(f"Check Result (raise=False): {is_win_safe}")
