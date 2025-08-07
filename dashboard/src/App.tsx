
import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function ProxyDashboard() {
  const [proxies, setProxies] = useState([]);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    fetch("/proxies_result.json")
      .then((res) => res.json())
      .then(setProxies)
      .catch(console.error);
  }, []);

  const filtered = proxies.filter(
    (p) =>
      p.server.includes(filter) ||
      p.ip.includes(filter) ||
      p.isp?.includes(filter)
  );

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">🧪 SOCKS5 Proxy Dashboard</h1>

      <Input
        placeholder="Search by IP, server, or ISP"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        className="w-full max-w-md"
      />

      <Card>
        <CardContent className="overflow-x-auto p-4">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>IP</TableHead>
                <TableHead>Ping</TableHead>
                <TableHead>Download</TableHead>
                <TableHead>Upload</TableHead>
                <TableHead>Country</TableHead>
                <TableHead>ISP</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map((proxy, i) => (
                <TableRow key={i}>
                  <TableCell>{proxy.ip}</TableCell>
                  <TableCell>{proxy.ping} ms</TableCell>
                  <TableCell>{proxy.download} Mbps</TableCell>
                  <TableCell>{proxy.upload} Mbps</TableCell>
                  <TableCell>{proxy.country}</TableCell>
                  <TableCell>{proxy.isp}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
