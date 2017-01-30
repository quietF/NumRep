
public class Distribution {

	public Distribution() {
		
	}
	
	public double evaluate(double x){
		double mu = 0.;
		double sd = 1.;
		return Math.exp(-(x-mu)*(x-mu) / (2 * sd * sd));
	}
	

}
