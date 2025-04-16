
import nmap

def scan_ports(target, top_ports=True):
    scanner = nmap.PortScanner()

    try:
        print("\n[+] Step 0: Scanning ports and services with Nmap...")
        print("    → Command used: nmap -sV{} {}".format(
            " --top-ports 1000" if top_ports else " -p-", target
        ))
        print("    → Tip: Start with top 1000 ports for speed. Use full range (-p-) if nothing is found.")

        args = "-sV"
        if top_ports:
            args += " --top-ports 1000"
        else:
            args += " -p-"

        scanner.scan(target, arguments=args)

        scan_data = []
        for host in scanner.all_hosts():
            for proto in scanner[host].all_protocols():
                lport = scanner[host][proto].keys()
                for port in sorted(lport):
                    service = scanner[host][proto][port]
                    scan_data.append({
                        "port": port,
                        "protocol": proto,
                        "state": service["state"],
                        "name": service["name"],
                        "product": service.get("product", ""),
                        "version": service.get("version", "")
                    })

        return scan_data

    except Exception as e:
        print("[!] Error during Nmap scan: {}".format(str(e)))
        return []
