import java.util.*;


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
	
	private double x0, x1, xb;
	private final double zeroish = 0.00001;
	public int steps = 0;
	
	Exception e2 = new Exception("Secant method will not converge.");
	Exception e1 = new Exception("Newton-Raphson method will not converge.");
	
	
	Function f_g_h;
	
	public Methods(Function f_g_h, Scanner choose) {
		this.f_g_h = f_g_h;
		this.setBoundaries(choose);
		
	}
	
	public void setBoundaries(Scanner choose){
		System.out.printf("\nChoose the range you want to look at (smallest x value first):\nx0: ");
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
	
	public boolean goodBoundaries(double x0, double x1){
		if(f_g_h.evaluate(x0)*f_g_h.evaluate(x1)>0.)
			return false;
		else return true;
	}
	
	public boolean foundRoot(double x){
		if(Math.abs(this.x1-this.x0)<=zeroish)  //(Math.abs(f_g_h.evaluate(x))<=zeroish)
			return true;
		else return false;
	}
	
	public ArrayList<ArrayList<Double>> findRootRanges(){
	    ArrayList<ArrayList<Double>> rootRange = new ArrayList<ArrayList<Double>>();
	    int N = 9, j=0;
	    double dx = (x1-x0)/N, x=x0;
	    for(int i=0; i<N; i++){
	        x=x0+i*dx;
	        if(f_g_h.evaluate(x)*f_g_h.evaluate(x+dx)<=0.){
	            rootRange.add(new ArrayList<Double>(Arrays.asList(x, x+dx)));
				System.out.println("Root found in range: " + x + ", " + (x+dx));
	            j+=1;
	        }
	    }
	    return rootRange;
	}
	
	public double findRoot_B(){
	    	this.steps += 1;
		this.xb = (x1+x0)/2.;
		double root = 0.;
		if(this.foundRoot(xb)) return xb;
		if(this.goodBoundaries(x0, xb)){
			this.x1 = xb;
			root = this.findRoot_B();
		} else if(this.goodBoundaries(xb, x1)){
			this.x0 = xb;
			root = this.findRoot_B();
		} else{
			System.out.println("Oh Oh...");
		}
		return root;
	}

	public double findRoot_NR() throws Exception{
	    
	    double dx = Math.abs(this.x1-this.x0)/10000., x0_aux = x0, x1_aux = x1;
	    double slope = (f_g_h.evaluate(x0+dx)-f_g_h.evaluate(x0))/dx;
		this.xb = x0-f_g_h.evaluate(x0)/slope;
		double root = xb;
		this.steps += 1;
		if(this.xb > x1_aux){
		    throw e1;
		} else if(this.foundRoot(xb)) return xb;
		else{
		    if(this.goodBoundaries(x0,xb)) this.x1 = xb;
		    else this.x0 = xb;
		    slope = (f_g_h.evaluate(x1)-f_g_h.evaluate(x1-dx))/dx;
		    this.xb = x1-f_g_h.evaluate(x1)/slope;
		    this.steps += 1;  
		    if(this.xb < x0_aux){
		        throw e1;
		    } else if(this.foundRoot(xb)) return xb;
		    else{
		        if(this.goodBoundaries(xb, x1)) this.x0 = xb;
		        else this.x1 = xb;
		        root = this.findRoot_NR();
		    }
		}
		return root;
	}
	
	public double findRoot_S() throws Exception{
	    double x0_aux = x0, x1_aux = x1;
	    double secant_slope = (f_g_h.evaluate(x1)-f_g_h.evaluate(x0))/(x1-x0);
	    this.xb = x0-f_g_h.evaluate(x0)/secant_slope;
	    double root = xb;
	    this.steps += 1;
	    if(this.xb > x1_aux){
	      throw e2;
	    } else if(this.foundRoot(xb)) return xb;
	    else{
	      if(this.goodBoundaries(x0,xb)) this.x1 = xb;
	      else this.x0 = xb;
	      secant_slope = (f_g_h.evaluate(x1)-f_g_h.evaluate(x0))/(x1-x0);
	      this.xb = x1-f_g_h.evaluate(x1)/secant_slope;
	      this.steps += 1;
	      if(this.xb < x0_aux){
		throw e2;
	      } else if(this.foundRoot(xb)) return xb;
	      else{
		if(this.goodBoundaries(xb, x1)) this.x0 = xb;
		else this.x1 = xb;
		root = this.findRoot_S();
	      }
	    }
	    return root;
	}
	
	public double[][] findAllRoots(){
	
	    ArrayList<ArrayList<Double>> rootRanges = this.findRootRanges();
	    ArrayList<Double> range = new ArrayList<Double>();
	    double[][] roots = new double[rootRanges.size()][8];
	    
	    for(int i=0; i<rootRanges.size(); i++){
	        range = rootRanges.get(i);
		this.x0 = range.get(0);
		this.x1 = range.get(1);
		roots[i][0] = this.findRoot_B();
		roots[i][1] = this.steps;
		System.out.println("Root found at " + roots[i][0] + " with " + roots[i][1] + " steps, using bisection method.");
		this.steps = 0;
		try{
		  roots[i][2] = this.findRoot_NR();
		  roots[i][3] = this.steps;
		  System.out.println("Root found at " + roots[i][2] + " with " + roots[i][3] + " steps, using Newton-Raphson method.");
		} catch(Exception e){
		  System.out.println(e1.getMessage());
		}
		try{
		  roots[i][4] = this.findRoot_S();
		  roots[i][5] = this.steps;
		  System.out.println("Root found at " + roots[i][4] + " with " + roots[i][5] + " steps, using secant method.");
		} catch(Exception e){
		  System.out.println(e2.getMessage());
		}
		
		roots[i][6] = this.HfindRoot_NRandB();
		roots[i][7] = this.steps;
		System.out.println("Root found at " + roots[i][6] + " with " + roots[i][7] + " steps, using hybrid NR+B method.");		

		this.steps = 0;
	    }
	    
	    
	    return roots;
	}
		
	public double step_B(){
		++steps;
		xb = (x1+x0)/2.;
		if(this.foundRoot(xb)) return xb;
		if(this.goodBoundaries(x0, xb)){
			x1 = xb;
			return xb;
		} else if(this.goodBoundaries(xb, x1)){
			x0 = xb;
			return xb;
		} else return 10000.;
	}

	public double step_NR() throws Exception{
		++steps;
		double dx = Math.abs(x1-x0)/10000.;
		double slope = (f_g_h.evaluate(x0+dx)-f_g_h.evaluate(x0))/dx;
		xb = x0-f_g_h.evaluate(x0)/slope;
		if(xb > x1 || xb < x0) throw e1;
		else{
			if(this.goodBoundaries(x0, xb)){x1 = xb; return xb;}
			else{x0 = xb; return xb;}
		}
	}

	public double step_S() throws Exception{
		++steps;
		double secant_slope = (f_g_h.evaluate(x1)-f_g_h.evaluate(x0))/(x1-x0);
		xb = x0-f_g_h.evaluate(x0)/secant_slope;
		if(xb > x1 || xb < x0) throw e1;
		else if(this.foundRoot(xb)) return xb;
		else if(this.goodBoundaries(x0, xb)){ 
			x1 = xb;
			return xb;
		} else if(this.goodBoundaries(xb, x1)){ 
			x1 = xb;
			return xb;
        	} else return 100000.;
	}

	public double HfindRoot_SandB(){
	    double root=xb;
		while(!this.foundRoot(root)){
			try{
				root = this.step_S();
				System.out.println("a");
			} catch(Exception e){
				root = this.step_B();
				root = this.step_B();
			}
			System.out.println(root);
		}
		System.out.println(steps);
	    return root;
	}
	
	public double HfindRoot_NRandB(){
	    	double root=xb;
		this.steps = 0;
		while(!this.foundRoot(root)){
			try{
				root = this.step_NR();
				this.steps+=1;
				//System.out.println(root);
			} catch(Exception e){
				System.out.println("NR didn't work");
				root = this.step_B();
				root = this.step_B();
				root = this.step_B();
				this.steps+=3;
			}
		}
		//System.out.println(steps);
	    	return root;
	}
	
	public static void main(String[] args) throws Exception {
		Scanner choose = new Scanner(System.in);
		System.out.printf("Choose the function: f, g, or h: ");
		char f = choose.next().charAt(0);
		Function f_x = new Function(f);
		Methods bisection = new Methods(f_x, choose);
		double[][] roots = bisection.findAllRoots();
		/*
		System.out.printf("Choose method: bisection (b), NewtonRaphson (n), Secant (s) or Hybrid NR+B (h)");
		char method = choose.next().charAt(0);
		if(method=='b') System.out.println(bisection.findRoot_B() + " " + bisection.steps);
		else if(method=='n') System.out.println(bisection.findRoot_NR() + " " + bisection.steps);
                else if(method=='s') System.out.println(bisection.findRoot_S() + " " + bisection.steps);
                else if(method=='h') System.out.println(bisection.HfindRoot_NRandB() + " " + bisection.steps);
		*/
	}
	

}
