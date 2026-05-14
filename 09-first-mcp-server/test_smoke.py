"""Smoke test for mcp_server.py — checks the module loads and tools exist.

Run with:  python3 test_smoke.py

Prerequisites:  pip install fastmcp

This is a minimal sanity check, not a functional test of the tools themselves
(which need real files and a Linux system to fully exercise).
"""
import sys
from pathlib import Path

# Allow importing mcp_server from the same directory
sys.path.insert(0, str(Path(__file__).parent))


def main():
    print("Running smoke tests for mcp_server.py...\n")

    # 1. Module imports
    try:
        import mcp_server
    except ModuleNotFoundError as e:
        if "fastmcp" in str(e):
            print(f"  ⚠️  SKIPPED: fastmcp not installed locally.")
            print(f"     Run: pip install fastmcp")
            print(f"     Then re-run this test.")
            return 0  # not a real failure for the smoke test
        raise
    print("  ✓ Module imports cleanly")

    # 2. The 4 advertised tools should be present and callable
    expected_tools = [
        "recent_errors",
        "git_status_all_projects",
        "next_appointment",
        "api_cost_today",
    ]
    for tool in expected_tools:
        assert hasattr(mcp_server, tool), f"Missing tool: {tool}"
        fn = getattr(mcp_server, tool)
        assert callable(fn), f"Tool {tool} is not callable"
    print(f"  ✓ All {len(expected_tools)} tools present and callable")

    # 3. Security allowlist
    assert hasattr(mcp_server, "ALLOWED_SERVICES"), "ALLOWED_SERVICES missing"
    assert isinstance(mcp_server.ALLOWED_SERVICES, set), "ALLOWED_SERVICES not a set"
    assert len(mcp_server.ALLOWED_SERVICES) > 0, "ALLOWED_SERVICES is empty"
    print(f"  ✓ ALLOWED_SERVICES present with {len(mcp_server.ALLOWED_SERVICES)} entries")

    # 4. MCP server instantiated
    assert hasattr(mcp_server, "mcp"), "mcp instance missing"
    print(f"  ✓ MCP server instantiated")

    print("\n✅ All smoke tests passed.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as e:
        print(f"\n❌ FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {type(e).__name__}: {e}")
        sys.exit(2)
