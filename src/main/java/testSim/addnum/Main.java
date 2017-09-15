package testSim.addnum;

import testSim.main.SimSettings;
import testSim.main.Simulation;
public class Main {
    public static void main(String[] args) {
        SimSettings.Builder settings = new SimSettings.Builder();
        settings.N_IROBOTS(4);
        settings.N_QUADCOPTERS(0);
        settings.TIC_TIME_RATE(2);
        settings.WAYPOINT_FILE("square.wpt");
        settings.DRAW_WAYPOINTS(false);
        settings.DRAW_WAYPOINT_NAMES(false);
        settings.DRAWER(new AddnumDrawer());
        Simulation sim = new Simulation(AddnumApp.class, settings.build());
        sim.start();
    }
}
