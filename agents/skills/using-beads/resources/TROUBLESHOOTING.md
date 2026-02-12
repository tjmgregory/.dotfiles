# Troubleshooting Guide

Common issues encountered when using bd and how to resolve them.

## Contents

- [Dependencies Not Persisting](#dependencies-not-persisting)
- [Status Updates Not Visible](#status-updates-not-visible)
- [Version Requirements](#version-requirements)

---

## Dependencies Not Persisting

### Symptom
```bash
bd dep add issue-2 issue-1 --type blocks
# Reports: ✓ Added dependency
bd show issue-2
# Shows: No dependencies listed
```

### Root Cause (Fixed in v0.15.0+)
This was a **bug in bd** (GitHub issue #101) where the daemon ignored dependencies during issue creation. **Fixed in bd v0.15.0** (Oct 21, 2025).

### Resolution

**1. Check your bd version:**
```bash
bd version
```

**2. If version < 0.15.0, update bd:**
```bash
brew upgrade bd
```

**3. Restart daemon after upgrade:**
```bash
pkill -f "bd daemon"
bd daemon start
```

**4. Test dependency creation:**
```bash
bd create "Test A" -t task
bd create "Test B" -t task
bd dep add <B-id> <A-id> --type blocks
bd show <B-id>
# Should show: "Depends on (1): → <A-id>"
```

### Still Not Working?

If dependencies still don't persist after updating:

1. **Check daemon is running:**
   ```bash
   ps aux | grep "bd daemon"
   ```

2. **Try without --no-daemon flag:**
   ```bash
   # Instead of: bd --no-daemon dep add ...
   # Use: bd dep add ...  (let daemon handle it)
   ```

3. **Report to beads GitHub** with:
   - `bd version` output
   - Operating system
   - Reproducible test case

---

## Status Updates Not Visible

### Symptom
```bash
bd --no-daemon update issue-1 --status in_progress
# Reports: ✓ Updated issue: issue-1
bd show issue-1
# Shows: Status: open (not in_progress!)
```

### Root Cause
This is **expected behavior** when using `--no-daemon`. The `--no-daemon` flag writes to JSONL but reads come from SQLite. The daemon syncs them periodically.

### Resolution

**Use daemon mode (recommended):**
```bash
# Don't use --no-daemon for CRUD operations
bd update issue-1 --status in_progress
bd show issue-1
# ✓ Status reflects immediately
```

---

## Version Requirements

### Minimum Version for Dependency Persistence

**Issue:** Dependencies created but don't appear in `bd show` or dependency tree.

**Fix:** Upgrade to **bd v0.15.0+** (released Oct 2025)

```bash
bd version
# Should show: bd version 0.15.0 or higher
```

---

## Quick Reference

| Problem | Quick Fix |
|---------|-----------|
| Dependencies not saving | Upgrade to bd v0.15.0+ |
| Status updates lag | Use daemon mode (not `--no-daemon`) |
