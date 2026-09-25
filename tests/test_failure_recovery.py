from event_platform import Event,EventBus
def test_failed_event_reaches_dlq_after_bounded_retries():
 b=EventBus(max_retries=1,base_delay=0);b.subscribe("x",lambda e:(_ for _ in ()).throw(RuntimeError("boom")))
 assert b.publish(Event("1","x",{}))=="dead-letter";assert len(b.dead_letters)==1