from __future__ import annotations

import asyncio
import time

import httpx
import requests

# Configuración básica
MAX_CONCURRENT_REQUESTS = 5  # Límite del semáforo
URLS = ["https://github.com" for _ in range(40)]


async def fetch_url_async(
    client: httpx.AsyncClient,
    url: str,
    semaphore: asyncio.Semaphore,
):
    async with semaphore:
        try:
            response = await client.get(url, timeout=10.0)
            print(f"Éxito: {url} -> Código {response.status_code}")
            return response.status_code
        except httpx.HTTPError as exc:
            print(f"Error al solicitar {url}: {exc}")
            return None


def fetch_url(url: str):
    try:
        response = requests.get(url, timeout=5)
        print(f"Éxito: {url} -> Código {response.status_code}")
        return response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la petición: {e}")


async def main():
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    inicio = time.time()
    async with httpx.AsyncClient() as client:
        tasks = [fetch_url_async(client, url, semaphore) for url in URLS]

        resultados = await asyncio.gather(*tasks)
        print(f"\nProceso finalizado. Total de respuestas: {len(resultados)}")
    fin = time.time()
    print("Tiempo async:", fin - inicio, "segundos")

    inicio = time.time()
    resultados_sync = [fetch_url(url) for url in URLS]
    print(f"\nProceso finalizado. Total de respuestas: {len(resultados_sync)}")
    fin = time.time()
    print("Tiempo sync:", fin - inicio, "segundos")


if __name__ == "__main__":
    asyncio.run(main())
