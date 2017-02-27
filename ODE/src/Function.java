
public class Function {
	
	private final double x_min = 0.;//, x_max = 4.;
	private int order = 1;
	private double[][] x_Ex_rho;
	private boolean charge;
	
	public Function() {
		charge = true;
	}
	
	public Function(int n, int order) {
		charge = false;
		this.order = order;
		Efield ElectricField = new Efield(2*n, order);
		x_Ex_rho = ElectricField.getElectricField();
	}
	
	public boolean getCharge(){
		return this.charge;
	}
	
	public double evaluate(double x, double y){
		if(x >= x_min){
			if(x < 1 || x >=3) return 0.;
			else if(x >= 1 && x < 2) return 1.;
			else return -1.;
		} else{
			System.out.println(x + ": Only possitive input values <= 4.");
			return 3.;
		}
	}
	
	public double evaluate(int i){
		/*
		 * This evaluates the function -E(x)
		 */
		return -x_Ex_rho[i][1];
	}
	
	public double getAnalytic(double x, boolean EField){
		if(EField){
			if((x>=0 && x<=1) || (x>=3 && x<=4))
				return 0;
			else if(x>1 && x<=2)
				return x-1.;
			else if(x>2 && x<3)
				return 3.-x;
			else
				return 0.;
		} else{
			if((x>=0 && x<=1))
				return 0;
			else if(x>1 && x<=2)
				return -0.5*(x-1.)*(x-1.);
			else if(x>2 && x<3)
				return 0.5*(x-3.)*(x-3.) - 1.;
			else if(x>=3 && x<=4)
				return -1;
			else
				return -1.;
		}
	}
	
	

}
