package testSim.linenew;

import java.util.HashMap;
import java.util.HashSet;
import edu.illinois.mitra.cyphyhouse.interfaces.MutualExclusion;
import java.util.List;
import java.util.Map;
import edu.illinois.mitra.cyphyhouse.functions.DSMMultipleAttr;
import edu.illinois.mitra.cyphyhouse.comms.RobotMessage;
import edu.illinois.mitra.cyphyhouse.gvh.GlobalVarHolder;
import edu.illinois.mitra.cyphyhouse.interfaces.LogicThread;
import edu.illinois.mitra.cyphyhouse.motion.MotionParameters;
import edu.illinois.mitra.cyphyhouse.motion.RRTNode;
import edu.illinois.mitra.cyphyhouse.motion.MotionParameters.COLAVOID_MODE_TYPE;
import edu.illinois.mitra.cyphyhouse.objects.ItemPosition;
import edu.illinois.mitra.cyphyhouse.objects.ObstacleList;
import edu.illinois.mitra.cyphyhouse.objects.PositionList;
import edu.illinois.mitra.cyphyhouse.interfaces.DSM;
import edu.illinois.mitra.cyphyhouse.functions.GroupSetMutex;

public class LinenewApp extends LogicThread {
    private static final String TAG = "Linenew App";
    private DSM dsm;
    
    int pid;
    private int numBots;

    int x;
    int y;
    int z;
    boolean pick;
    boolean go;
    boolean wait;
    ItemPosition target;
    ItemPosition position;
        
    public LinenewApp (GlobalVarHolder gvh) {
        super(gvh);
        MotionParameters.Builder settings = new MotionParameters.Builder();
        settings.COLAVOID_MODE(COLAVOID_MODE_TYPE.USE_COLBACK);
        MotionParameters param = settings.build();
        gvh.plat.moat.setParameters(param);
        
        pid = Integer.parseInt(name.replaceAll("[^0-9]", ""));
        numBots = gvh.id.getParticipants().size();
        dsm = new DSMMultipleAttr(gvh);
    }
    @Override
    public List<Object> callStarL() {
        
        position = gvh.gps.getMyPosition();
        x = position.getX();
        dsm.put("x"+name,name,x);
        y = position.getY();
        dsm.put("y"+name,name,y);
        z = position.getZ();
        dsm.put("z"+name,name,z);
        pick = true;
        go = false;
        wait = false;
        
        while(true) {
            if (target != null) {gvh.plat.moat.goTo(target);}
            sleep(100);
                if (pick){
                
                    if(((pid == 0) || (pid == (numBots - 1)))) {
                        return null;
                    }
                    else {
                        if (dsm.get("x",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 ))) == null) {continue;}
                        x = Integer.parseInt(dsm.get("x",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 ))));
                        
                        if (dsm.get("x",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))) == null) {continue;}
                        x = Integer.parseInt(dsm.get("x",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))));
                        
                        if (dsm.get("y",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 ))) == null) {continue;}
                        y = Integer.parseInt(dsm.get("y",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 ))));
                        
                        if (dsm.get("y",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))) == null) {continue;}
                        y = Integer.parseInt(dsm.get("y",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))));
                        
                        if (dsm.get("z",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 ))) == null) {continue;}
                        z = Integer.parseInt(dsm.get("z",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 ))));
                        
                        if (dsm.get("z",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))) == null) {continue;}
                        z = Integer.parseInt(dsm.get("z",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))));
                        
                        target = new ItemPosition("temp",((Integer.parseInt(dsm.get("x",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 )))) + Integer.parseInt(dsm.get("x",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))))) / 2), ((Integer.parseInt(dsm.get("y",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 )))) + Integer.parseInt(dsm.get("y",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))))) / 2), ((Integer.parseInt(dsm.get("z",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 )))) + Integer.parseInt(dsm.get("z",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))))) / 2));
                        pick = false;
                        go = true;
                    }
                    
                    continue;
                }
                if (go){
                
                    position = gvh.gps.getMyPosition();
                    x = position.getX();
                    dsm.put("x"+name,name,x);
                    y = position.getY();
                    dsm.put("y"+name,name,y);
                    z = position.getZ();
                    dsm.put("z"+name,name,z);
                    if(!(gvh.plat.moat.inMotion)) {
                        go = false;
                        wait = true;
                    }
                    
                    continue;
                }
                if (wait){
                
                    if(gvh.plat.moat.done) {
                        wait = false;
                        pick = true;
                    }
                    
                    continue;
                }
        }
    }
    @Override
    protected void receive(RobotMessage m) {
    }
}