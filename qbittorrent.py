# qbittorrent_client.py
import qbittorrentapi

def enviar_a_qbittorrent(torrent_url, download_dir="movies/"):
    try:
        qbt_client = qbittorrentapi.Client(
            host="http://192.168.1.185/",
            port=15080,
            username="admin",
            password="mZVM2WnsL"
        )
        qbt_client.auth_log_in()

        print(f"Descargando en : {download_dir}")

        qbt_client.torrents_add(
            urls=torrent_url,
            save_path=download_dir,
            is_paused=False,
            category="movies"
        )
        return True
    except Exception as e:
        print("Error al añadir el torrent:", e)
        return False
