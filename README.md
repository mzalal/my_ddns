# myDDNS

A simple script that works as a self-hosted Dynamic DNS (DDNS) by checking the checking the network's current public IP address, comparing it with the content of a DNS record on Cloudflare, then then updating the DNS record if necessary.

> [!IMPORTANT]
> As it is now, this script only works with Cloudflare as a DNS provider/registrar.

## Requirements

- Python 3.9+
- cloudflare (cloudflare-python)
- requests
- python-dotenv

## Setup

1. Clone this repository and navigate into it

   ```sh
   git clone https://github.com/mzalal/my_ddns
   cd my_ddns
   ```

2. Create a virtual environment and activate it

   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```

   > [!TIP]
   > Depending on your system, you may need to use `python3` instead of `python`.

3. Install dependencies

   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following environment variables

   ```sh
   # The API token should have DNS edit permissions
   CLOUDFLARE_API_TOKEN=API_TOKEN_HERE

   # The DNS record name (domain/subdomain)
   DNS_RECORD_NAME=example.com
   # The ID of the DNS record
   CLOUDFLARE_DNS_RECORD_ID=DNS_RECORD_ID_HERE
   # The ID of the zone the DNS record belongs to
   CLOUDFLARE_ZONE_ID=ZONE_ID_HERE
   ```

5. Run the script

   ```sh
   python my_ddns.py
   ```

   If the script executed successfully, you should seen no output, and your console prompt should appear again after the script is done.
   Otherwise, you should check the log file (`my_ddns.log`) that is generated in the same directory as the script itself.

## myDDNS as a system service

To get the most of myDDNS, you can run it as a system service through systemd or as a cron job. And to automatically run myDDNS on 1 minute time intervals using systemd, create the following two files in `/etc/systemd/system`:

- `my-ddns.service`:

  ```ini
  [Unit]
  Description=myDDNS
  After=network-online.target
  Wants=network-online.target

  [Service]
  Type=oneshot
  # Change depending on where you placed .venv and my_ddns.py
  ExecStart=/path/to/python/executable /path/to/my_ddns.py

  [Install]
  WantedBy=multi-user.target
  ```

- `my-ddns.timer`:

  ```ini
  [Unit]
  Description=Run my-ddns.service 10s after boot and every 1m after that

  [Timer]
  # Run my-ddns.service 10 seconds after the system boots
  OnBootSec=10s
  # Then run it every minute after that
  OnUnitActiveSec=1m
  Unit=my-ddns.service

  [Install]
  WantedBy=timers.target
  ```

Then start and enable `my-ddns.timer`:

```sh
sudo systemctl start my-ddns.timer
sudo systemctl enable my-ddns.timer
```

## License

myDDNS is licensed under the MIT license.
