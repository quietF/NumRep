//
//  TestMyIO.java
//  
//
//  Created by PeterClarke on 25/06/2013.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

import Jama.*;

//To use and test the simple IO package

public final class TestMyIO {
	
	public static final void main(String... aArgs){
		log("Testing MyIO ");
		
		
		// Test the file reader
		if( true ) {

		log("Reading file testfile.txt");

		MyFileReader handle = new MyFileReader("testfile.txt") ;
		handle.print();
		
		log("The matrix returned was ");
		
		Matrix M = handle.getMatrix();
		M.print(5,3);
				
		Matrix C1 = handle.getColumn( 0 ) ;		
		C1.print(5,3) ;

		Matrix C2 = handle.getColumn( 1 ) ;		
		C2.print(5,3) ;
			
		}


		// Test the file writer
		if( true ) {
			
			MyFileWriter handleout = new MyFileWriter() ;
			
			Matrix M =new Matrix(5,3) ;

			log("Writing file testout.txt");
			
			handleout.writeFile( "testout.txt", M) ;
			
		}
		
		
	}	
	
	private static void log(String aMessage){
		System.out.println(aMessage);
	}
	
}
