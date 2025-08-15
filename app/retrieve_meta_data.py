import a2s
import socket
import time

# This script retrieves metadata from a game server using the Valve A2S protocol.
SERVER_ADDRESS = ("35.154.230.209", 27015)

def fmt_duration(sec: float) -> str:
    try:
        sec = int(sec)
    except Exception:
        return f"{sec:.1f}s"
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def main():
    try:
        # Measure RTT as a proxy for ping
        start = time.perf_counter()
        info = a2s.info(SERVER_ADDRESS, timeout=3.0)
        ping_ms = (time.perf_counter() - start) * 1000

        print("=== Server Info ===")
        print(f"Name: {info.server_name}")
        print(f"Map: {info.map_name}")
        print(f"Players: {info.player_count}/{info.max_players} (bots: {info.bot_count})")
        print(f"Game: {info.game}")
        vac = getattr(info, "vac_enabled", None)
        if vac is not None:
            print(f"VAC enabled: {vac}")
        print(f"Ping: {ping_ms:.0f} ms")

        # print("\n=== Players ===")
        # try:
        #     players = a2s.players(SERVER_ADDRESS, timeout=3.0)
        #     if not players:
        #         print("(no players)")
        #     else:
        #         for p in sorted(players, key=lambda x: (-x.score, x.name or "")):
        #             name = p.name or "(unnamed)"
        #             print(f"{name} - {p.score} kills, {fmt_duration(p.duration)}")
        # except Exception as e:
        #     print(f"Could not retrieve player list (server may not allow A2S_PLAYER): {e}")

    except (a2s.BrokenMessageError, a2s.BufferExhaustedError, a2s.ConnectionError, socket.timeout) as e:
        print(f"Query failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()