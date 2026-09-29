import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from event_domain import Event, IdempotencyStore, retry_delay
e=Event.create("orders","o-1",{"x":1}); s=IdempotencyStore(); report={"first_seen":s.first_seen(e.event_id),"duplicate_seen":s.first_seen(e.event_id),"retry_delays":[retry_delay(i) for i in range(4)]}
if not report["first_seen"] or report["duplicate_seen"] or report["retry_delays"]!=[0.5,1.0,2.0,4.0]: raise SystemExit(report)
print(json.dumps(report, sort_keys=True))
