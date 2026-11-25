# Portable Agent Roles

These files do not require a specific AI provider or agent API. Shared working rules are in `../AGENTS.md`; detailed technical rules are in `../Hardware-Rules.md` and `../Hardware-Roles.md`.

## If automatic agent support exists

The Manager stays in the main session; when needed it starts the Designer and Reviewer roles with the right model. Verify the client's capabilities and the supported model/effort settings. Platform adapters are only a convenience; the shared role files work in every client.

## If there is no automatic agent support / the AI is being changed

1. The Manager prepares a short task package from the current project records (`Hardware-Roles.md` §05).
2. The user gives the relevant role file and the required project files to the AI session of their choice.
3. The user passes the task result, the real file changes and the review evidence back to the Manager.
4. The Manager runs the next stage, keeping the current revision and approvals.

Example prompt:

> Follow the AGENTS.md and agents/Reviewer.md instructions. Review the assigned design revision and only the relevant files. Do not change the Designer's design. Report real findings briefly; report anything you could not verify as BLOCKED.

To continue with a different AI there is no need to resend the whole chat. The project files are the shared source of record. In a client that cannot access files or the EDA tool, the rule of not presenting actions as done still applies.
