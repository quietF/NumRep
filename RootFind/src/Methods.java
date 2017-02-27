import java.util.Scanner;

public class Methods {
	/*
	 * Root finding with different methods:
	 * i) Bisection
	 * ii) Newton-Raphson
	 * iii) Secant
	 * 
	 * receiving a function through a class in
	 * Function.java 
	 */
	
	private double x0, x1;
	private final double zeroish = 0.0001;
	Function f_g_h;
	
	public Methods(Function f_g_h, Scanner choose) {
		this.f_g_h = f_g_h;
		this.setBoundaries(choose);
		
	}
	
	public void setBoundaries(Scanner choose){
		System.out.printf("\nChoose the range you want to look at:\nx0: ");
		double x0 = choose.nextDouble();
		System.out.printf("x1: ");
		double x1 = choose.nextDouble();
		this.x0 = x0;
		this.x1 = x1;
		while(!this.goodBoundaries()){
			System.out.printf("\nChange range.");
			this.setBoundaries(choose);
		}
		if(this.foundRoot(x0) || this.foundRoot(x1)){
			System.out.println("Root found!");
			if(this.foundRoot(x0)) System.out.println("f("+x0+")=0");
			else System.out.println("f("+x1+")=0");
		}
	}
	
	public boolean goodBoundaries(){
		if(f_g_h.evaluate(x0)*f_g_h.evaluate(x1)>0.)
			return false;
		else return true;
	}
	
	public boolean foundRoot(double x){
		if(Math.abs(f_g_h.evaluate(x))<=zeroish)
			return true;
		else return false;
	}
	
	public double findRoot_B(){
		double xb = (x1-x0)/2., x0_aux = x0, root = 0.;
		
		return root;
	}
	
	public static void main(String[] args) throws Exception {
		Scanner choose = new Scanner(System.in);
		System.out.printf("Choose the function: f, g, or h: ");
		char f = choose.next().charAt(0);
		Function f_x = new Function(f);
		Methods bisection = new Methods(f_x, choose);
		double root = bisection.findRoot_B();
		System.out.println(root);
	}
	

}
