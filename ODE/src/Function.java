
public class Function {
	
	private final double x_min = 0., x_max = 4.;
	
	public Function() {
		
	}
	
	public double evaluateChargeDensity(double x, double y){
		if(x >= x_min){
			if(x < 1 || x >=3) return 0.;
			else if(x >= 1 && x < 2) return 1.;
			else return -1.;
		} else{
			System.out.println(x + ": Only possitive input values <= 4.");
		}
		return 3.;
	}

}
