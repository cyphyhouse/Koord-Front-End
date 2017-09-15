package testSim.leaderelect;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

import edu.illinois.mitra.cyphyhouse.comms.RobotMessage;
import edu.illinois.mitra.cyphyhouse.gvh.GlobalVarHolder;
import edu.illinois.mitra.cyphyhouse.interfaces.LogicThread;
import edu.illinois.mitra.cyphyhouse.objects.ItemPosition;


import edu.illinois.mitra.cyphyhouse.interfaces.MutualExclusion;
import edu.illinois.mitra.cyphyhouse.functions.DSMMultipleAttr;
import edu.illinois.mitra.cyphyhouse.functions.GroupSetMutex;
import edu.illinois.mitra.cyphyhouse.functions.SingleHopMutualExclusion;
import edu.illinois.mitra.cyphyhouse.interfaces.DSM;


public class LeaderelectApp extends LogicThread {
    private static final String TAG = "Leaderelect App";
    int pid;
    private int numBots;
    private MutualExclusion mutex0;
    
    private DSM dsm;
    

    public int currCand = -1;
    public int numVoted = 0;


     boolean voted = false;
     int myCand = -1;
     int leader = -1;
        private boolean wait0 = false;
    public LeaderelectApp (GlobalVarHolder gvh){
        super(gvh);
        pid = Integer.parseInt(name.replaceAll("[^0-9]", ""));
        numBots = gvh.id.getParticipants().size();
        mutex0= new GroupSetMutex(gvh, 0);
        dsm = new DSMMultipleAttr(gvh);
        
        
        myCand = pid;
        
    }
    
    @Override
    public List<Object> callStarL() {
        dsm.createMW("currCand",0);
        dsm.createMW("numVoted",0);
        
        while(true) {
            sleep(100);
            
            if ((!(voted))){
            
                if(!wait0){
                
                    mutex0.requestEntry(0);
                    wait0 = true;
                    
                }
                if (mutex0.clearToEnter(0)) {
                
                    
                    currCand = Integer.parseInt(dsm.get("currCand","*"));
                    if((myCand)>(currCand)){
                        
                        currCand = myCand;
                        dsm.put("currCand","*",currCand);
                    }
                    else {
                        
                        currCand = myCand;
                        dsm.put("currCand","*",currCand);
                    }
                    
                    voted = true;
                    
                    numVoted = Integer.parseInt(dsm.get("numVoted","*"));
                    numVoted = ( numVoted + 1 );
                    dsm.put("numVoted","*",numVoted);
                    mutex0.exit(0);
                    
                }
                
                continue;
                
            }
            
            numVoted = Integer.parseInt(dsm.get("numVoted","*"));
            
            if (((voted)&&( (numVoted) < (numBots) ))){
            
                currCand = Integer.parseInt(dsm.get("currCand","*"));
                myCand = currCand;
                
                continue;
                
            }
            numVoted = Integer.parseInt(dsm.get("numVoted","*"));
            
            if (((numVoted)==(numBots))){
            
                currCand = Integer.parseInt(dsm.get("currCand","*"));
                leader = currCand;
                
                continue;
                
            }
        }
    }
    @Override
    protected void receive(RobotMessage m) {
	return;
   }
}
