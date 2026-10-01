import {describe,it,expect,vi} from 'vitest';
import {locationSession} from './location-session';

function setup(){
  let receive:PositionCallback=()=>{};let fail:PositionErrorCallback=()=>{};
  const service={watchPosition:vi.fn((next:PositionCallback,error?:PositionErrorCallback|null)=>{receive=next;fail=error??(()=>{});return 7}),clearWatch:vi.fn()};
  const update=vi.fn(),error=vi.fn();
  const session=locationSession(service,update,error);
  const position={coords:{latitude:28.6,longitude:77.2,accuracy:30}} as GeolocationPosition;
  return {service,update,error,session,emit:()=>receive(position),fail:()=>fail({code:1} as GeolocationPositionError)};
}
describe('location watch lifecycle',()=>{
  it('requests high accuracy only after an explicit start and keeps it configurable',()=>{
    const service={watchPosition:vi.fn(()=>5),clearWatch:vi.fn()};
    const session=locationSession(service,vi.fn(),vi.fn(),{enableHighAccuracy:true,maximumAge:5000,timeout:20000});
    expect(service.watchPosition).not.toHaveBeenCalled();session.start();
    expect(service.watchPosition).toHaveBeenCalledWith(expect.any(Function),expect.any(Function),{enableHighAccuracy:true,maximumAge:5000,timeout:20000});
    session.stop();expect(service.clearWatch).toHaveBeenCalledWith(5);
  });
  it('clears positions and ignores queued updates after stopping',()=>{
    const s=setup();s.session.start();s.emit();s.session.stop();s.emit();
    expect(s.update.mock.calls).toEqual([[{lat:28.6,lng:77.2,accuracy:30}],[null]]);
    expect(s.service.clearWatch).toHaveBeenCalledWith(7);
  });
  it('clears an earlier position when a watch fails and does not restart itself',()=>{
    const s=setup();s.session.start();s.emit();s.fail();s.emit();
    expect(s.update).toHaveBeenLastCalledWith(null);expect(s.error).toHaveBeenCalledOnce();
    expect(s.service.watchPosition).toHaveBeenCalledOnce();
  });
  it('does not create duplicate watches and supports a deliberate restart',()=>{
    const s=setup();s.session.start();s.session.start();expect(s.service.watchPosition).toHaveBeenCalledOnce();
    s.session.stop();s.session.start();s.emit();expect(s.service.watchPosition).toHaveBeenCalledTimes(2);
  });
});
