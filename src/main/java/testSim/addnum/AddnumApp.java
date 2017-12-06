package testSim.addnum;

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

public class AddnumApp extends LogicThread {
    private static final String TAG = "Addnum App";
    private MutualExclusion mutex0;
    
    private DSM dsm;
    
    int pid;
    private int numBots;

    int sum = 0;
    int numadded = 0;
    boolean added = false;
    int finalsum;
        private boolean wait0 = false;
    public AddnumApp (GlobalVarHolder gvh) {
        super(gvh);
        MotionParameters.Builder settings = new MotionParameters.Builder();
        settings.COLAVOID_MODE(COLAVOID_MODE_TYPE.USE_COLBACK);
        MotionParameters param = settings.build();
        gvh.plat.moat.setParameters(param);
        
        pid = Integer.parseInt(name.replaceAll("[^0-9]", ""));
        numBots = gvh.id.getParticipants().size();
        dsm = new DSMMultipleAttr(gvh);mutex0 = new GroupSetMutex(gvh,0);
        
    }
    @Override
    public List<Object> callStarL() {
        dsm.createMW("sum",0);
        dsm.createMW("numadded",0);
        
        while(true) {
            sleep(100);
                if (!(added)){
                
                    if(!wait0){
                    
                        mutex0.requestEntry(0);
                        wait0 = true;
                        
                    }
                    if (mutex0.clearToEnter(0)) {
                    
                        if (dsm.get("sum","*") == null) {continue;}
                        sum = Integer.parseInt(dsm.get("sum","*"));
                        
                        sum = (sum + (pid * 2));
                        dsm.put("sum","*",sum);
                        if (dsm.get("numadded","*") == null) {continue;}
                        numadded = Integer.parseInt(dsm.get("numadded","*"));
                        
                        numadded = (numadded + 1);
                        dsm.put("numadded","*",numadded);
                        added = true;
                        mutex0.exit(0);
                        
                    }
                    
                    continue;
                }
                if (dsm.get("numadded","*") == null) {continue;}
                numadded = Integer.parseInt(dsm.get("numadded","*"));
                
                if ((numadded == numBots)){
                
                    if (dsm.get("sum","*") == null) {continue;}
                    sum = Integer.parseInt(dsm.get("sum","*"));
                    
                    finalsum = sum;
                    continue;
                }
        }
    }
    @Override
    protected void receive(RobotMessage m) {
    }
}