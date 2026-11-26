# MCP setup

How the AI connects to your EDA tool. The AI asks which EDA tool you use (INT-04), then offers to set up the matching MCP server (INT-54). Nothing is installed without your explicit yes.

## Rules

- The AI shows each command before it runs it and installs only after you say yes.
- You enter license keys, sign-ins and passwords yourself. The AI never types them.
- Pick a scope:
  - **This project only (recommended):** the server is available only in this project folder.
  - **All my projects:** the server is available everywhere for your user account.
- MCP is registered in your **AI client** (Claude Code, Claude Desktop, Codex, Cursor, Gemini CLI …), not inside the board files.
- Config files contain local paths. Do not commit them unless every user has the same setup.
- After setup, the AI checks the connection with a real read call (list tools, open the project) and records server, version and scope in `Project-README.md` → "EDA & Tool Integration".
- The Reviewer uses a read-only connection (REV-13).
- No tool access (web chat) or you said no: the AI gives manual steps and you work in the EDA tool yourself.

## Which server

| EDA | Suggested server | Needs |
| :--- | :--- | :--- |
| KiCad | [KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server) (`stable` branch) | KiCad 9.0+, Node.js 18+, Python (see its README) |
| Altium Designer | [Official Altium MCP Server](https://docs.developer.altium.com/ad-mcp-docs/) | Altium Designer 26.5+, MCP add-on license |
| Altium Designer (alternative) | [altium-mcp](https://github.com/coffeenmusic/altium-mcp) | Python 3.10–3.14; installed as a Claude Desktop extension |
| EasyEDA Pro | [Extension API](https://prodocs.easyeda.com/en/api/guide/); third-party MCP only on request | — |

Always check the server's own README for the current steps; the summaries below can age.

## KiCad (KiCAD-MCP-Server)

1. Build the server:

```bash
git clone --branch stable https://github.com/mixelpixx/KiCAD-MCP-Server.git
cd KiCAD-MCP-Server
npm install
npm run build
pip3 install -r requirements.txt
```

On Windows the repo also has `.\setup-windows.ps1`.

2. Register it in your AI client. Use two entries: `kicad` for the Designer (writes) and `kicad-readonly` for the Reviewer.

Claude Code (default scope = this project only, private; `--scope user` = all projects; `--scope project` writes a shared `.mcp.json`):

```bash
claude mcp add --env KICAD_MCP_TOOLBOXES=core --env PYTHONPATH="<KiCad python path>" kicad -- node <path>/KiCAD-MCP-Server/dist/index.js
claude mcp add --env KICAD_MCP_OPERATING_MODE=readonly --env KICAD_MCP_TOOLBOXES=core --env PYTHONPATH="<KiCad python path>" kicad-readonly -- node <path>/KiCAD-MCP-Server/dist/index.js
```

Other clients use the same `mcpServers` JSON block. See [examples/mcp/kicad.mcp.example.json](examples/mcp/kicad.mcp.example.json). Where it goes:

| Client | This project only | All projects |
| :--- | :--- | :--- |
| Claude Code | `claude mcp add` (default scope) or `.mcp.json` | `claude mcp add --scope user` |
| Claude Desktop | — | `claude_desktop_config.json` |
| Cursor | `.cursor/mcp.json` | user settings |
| Gemini CLI | `.gemini/settings.json` | `~/.gemini/settings.json` |
| Codex | see the Codex MCP docs | `~/.codex/config.toml` |

Example `PYTHONPATH` on Windows: `C:\Program Files\KiCad\9.0\lib\python3\dist-packages`.

Useful settings: `KICAD_MCP_TOOLBOXES=core` saves tokens; `KICAD_MCP_OPERATING_MODE` is `write` (default), `readonly` or `manufacturing` (read-only plus export).

## Altium Designer

**Official server:** in Altium Designer open Extensions and Updates → install **MCP Server** → restart. Then Preferences → Data Management → MCP Server → tick **Enable MCP Server** → Client Connections → pick your client → **Install** → restart the AI client. A license and an Altium 365 workspace may be needed; you handle those.

**altium-mcp:** download `altium-mcp.dxt` from its releases and install it in Claude Desktop (Settings → Extensions → Advanced → Install Extension). It has no read-only mode; the Reviewer uses only read and check tools (REV-13).

## Check

Ask the AI to list the server's tools and open your project read-only. If that fails, the AI reports BLOCKED with the error and does not pretend the tool works.
