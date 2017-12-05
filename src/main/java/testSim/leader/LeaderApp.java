package testSim.leader;

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

public class LeaderApp extends LogicThread {
    private static final String TAG = "Leader App";
    private MutualExclusion mutex0;
    
    private DSM dsm;
    
    int pid;
    private int numBots;

    int candidate = -1;
    boolean voted = false;
    int leader;
        private boolean wait0 = false;
    public LeaderApp (GlobalVarHolder gvh) {
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
        dsm.createMW("candidate",0);
        
        while(true) {
            sleep(100);
                if (!(voted)){
                
                    if(!wait0){
                    
                        mutex0.requestEntry(0);
                        wait0 = true;
                        
                    }
                    if (mutex0.clearToEnter(0)) {
                    
                        if((candidate < pid)) {
                            candidate = pid;
                            dsm.put("candidate","*",candidate);
                        }
                        else {
                            if (dsm.get("candidate","*") == null) {continue;}
                            candidate = Integer.parseInt(dsm.get("candidate","*"));
                            
                            leader = candidate;
                            dsm.put("leader","*",leader);
                        }
                        
                        voted = true;
                        mutex0.exit(0);
                        
                    }
                    
                    continue;
                }
                if (voted){
                
                    if (dsm.get("candidate","*") == null) {continue;}
                    candidate = Integer.parseInt(dsm.get("candidate","*"));
                    
                    leader = candidate;
                    dsm.put("leader","*",leader);
                    continue;
                }
        }
    }
    @Override
    protected void receive(RobotMessage m) {
    }
}