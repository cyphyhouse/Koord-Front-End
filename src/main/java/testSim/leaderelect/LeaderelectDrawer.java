package testSim.leaderelect;import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Stroke;
import org.apache.log4j.Logger;

import edu.illinois.mitra.cyphyhouse.interfaces.LogicThread;
import testSim.draw.Drawer;

public class LeaderelectDrawer extends Drawer {
    private Stroke stroke = new BasicStroke(8);
    private Color selectColor = new Color(0,0,255,100);
    private static org.apache.log4j.Logger log = Logger.getLogger(LeaderelectDrawer.class);
    @Override
    public void draw(LogicThread lt, Graphics2D g) {
        LeaderelectApp app = (LeaderelectApp) lt;
        g.setColor(Color.RED);
        g.setColor(selectColor);
        g.setStroke(stroke);
        //log.info("pid:" + String.valueOf(app.pid)+" myCand :"+String.valueOf(app.myCand) + "leader :"+String.valueOf(app.leader));
        log.info("numVoted:" + String.valueOf(app.numVoted));
        log.info("id:" + String.valueOf(app.pid) + String.valueOf(app.myCand));
        //g.drawString("current total "+String.valueOf(app.currentTotal),100+10*app.robotIndex,150);
    }
}
