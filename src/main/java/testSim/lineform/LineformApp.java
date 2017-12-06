package testSim.lineform;

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

public class LineformApp extends LogicThread {
    private static final String TAG = "Lineform App";
    private DSM dsm;
    
    int pid;
    private int numBots;

    private enum Stage { 
        PICK, GO, WAIT
    };
    private Stage stage;
    
    int x;
    int y;
    int z;
    ItemPosition target;
    ItemPosition position;
        
    public LineformApp (GlobalVarHolder gvh) {
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
        stage = Stage.PICK;
        
        while(true) {
            position = gvh.gps.getMyPosition();
            if (target != null) {gvh.plat.moat.goTo(target);}
            sleep(100);
            switch(stage) {
                case PICK:
                
                    if(((pid == 0) || (pid == (numBots - 1)))) {
                        return null;
                    }
                    else {
                        if (dsm.get("x",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 ))) == null) {break;}
                        x = Integer.parseInt(dsm.get("x",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 ))));
                        
                        if (dsm.get("x",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))) == null) {break;}
                        x = Integer.parseInt(dsm.get("x",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))));
                        
                        if (dsm.get("y",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 ))) == null) {break;}
                        y = Integer.parseInt(dsm.get("y",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 ))));
                        
                        if (dsm.get("y",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))) == null) {break;}
                        y = Integer.parseInt(dsm.get("y",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))));
                        
                        if (dsm.get("z",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 ))) == null) {break;}
                        z = Integer.parseInt(dsm.get("z",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 ))));
                        
                        if (dsm.get("z",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))) == null) {break;}
                        z = Integer.parseInt(dsm.get("z",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))));
                        
                        target = new ItemPosition("temp",((Integer.parseInt(dsm.get("x",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 )))) + Integer.parseInt(dsm.get("x",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))))) / 2), ((Integer.parseInt(dsm.get("y",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 )))) + Integer.parseInt(dsm.get("y",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))))) / 2), ((Integer.parseInt(dsm.get("z",name.replaceAll("[0-9]","")+String.valueOf(( pid - 1 )))) + Integer.parseInt(dsm.get("z",name.replaceAll("[0-9]","")+String.valueOf(( pid + 1 ))))) / 2));
                        stage = Stage.GO;
                    }
                    
                break;
                case GO:
                
                    x = position.getX();
                    dsm.put("x"+name,name,x);
                    y = position.getY();
                    dsm.put("y"+name,name,y);
                    z = position.getZ();
                    dsm.put("z"+name,name,z);
                    if(!(gvh.plat.moat.inMotion)) {
                        stage = Stage.WAIT;
                    }
                    
                break;
                case WAIT:
                
                    if(gvh.plat.moat.done) {
                        stage = Stage.PICK;
                    }
                    
                break;
            }
        }
    }
    @Override
    protected void receive(RobotMessage m) {
    }
}
