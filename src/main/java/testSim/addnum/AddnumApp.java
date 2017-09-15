package testSim.addnum;

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


public class AddnumApp extends LogicThread {
    private static final String TAG = "Addnum App";
    int pid;
    private int numBots;
    private MutualExclusion mutex0;
    
    private DSM dsm;
    

    public int sum = 0;
    public int numadded = 0;


     boolean added = false;
     int finalsum;
    private boolean wait0 = false;
    public AddnumApp (GlobalVarHolder gvh){
        super(gvh);
        pid = Integer.parseInt(name.replaceAll("[^0-9]", ""));
        numBots = gvh.id.getParticipants().size();
        mutex0= new GroupSetMutex(gvh, 0);
        dsm = new DSMMultipleAttr(gvh);
        
    }
    
    @Override
    public List<Object> callStarL() {
        dsm.createMW("sum",0);
        dsm.createMW("numadded",0);
        
        while(true) {
            sleep(100);
            
            if ((!(added))){
            
                if(!wait0){
                
                    mutex0.requestEntry(0);
                    wait0 = true;
                    
                }
                if (mutex0.clearToEnter(0)) {
                
                    sum = Integer.parseInt(dsm.get("sum","*"));
                    
                    sum = ( sum + ( pid * 2 ) );
                    dsm.put("sum","*",sum);
                    numadded = Integer.parseInt(dsm.get("numadded","*"));
                    numadded = ( numadded + 1 );
                    dsm.put("numadded","*",numadded);
                    added = true;
                    
                    mutex0.exit(0);
                    
                }
                
                continue;
                
            }
            
            numadded = Integer.parseInt(dsm.get("numadded","*"));
            
            if (((added)&&( (numadded) < (numBots) ))){
            
                continue;
                
            }
            numadded = Integer.parseInt(dsm.get("numadded","*"));
            
            if (((numadded)==(numBots))){
            
                sum = Integer.parseInt(dsm.get("sum","*"));
                finalsum = sum;
                
                continue;
                
            }
        }
    }
    @Override
    protected void receive(RobotMessage m) {
	return;
   }
}
