
public class Function {
	
	private final double x_min = 0.;//, x_max = 4.;
	private int order = 1;
	public double[][] x_Ex_rho;
	public boolean charge;
	
	public Function() {
		charge = true;
	}
	
	public Function(int n, int order) {
		charge = false;
		this.order = order;
		Efield ElectricField = new Efield(n, order);
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
	
	public double evaluate(int i_x, int i_y){
		return x_Ex_rho[i_x][1];
	}
	
	

}
