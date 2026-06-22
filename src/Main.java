import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        HospitalService hs = new HospitalService();
        int choice;

        do {
            System.out.println("\n======= HOSPITAL MANAGEMENT SYSTEM =======");
            System.out.println("1. Add Patient");
            System.out.println("2. Add Doctor");
            System.out.println("3. Book Appointment");
            System.out.println("4. View All Patients");
            System.out.println("5. View All Doctors");
            System.out.println("6. View All Appointments");
            System.out.println("0. Exit");
            System.out.print("Enter choice: ");
            choice = sc.nextInt(); sc.nextLine();

            switch (choice) {
                case 1 -> {
                    System.out.print("Enter Patient Name: ");
                    String pname = sc.nextLine();
                    System.out.print("Enter Age: ");
                    int age = sc.nextInt(); sc.nextLine();
                    System.out.print("Enter Disease: ");
                    String disease = sc.nextLine();
                    hs.addPatient(pname, age, disease);
                }
                case 2 -> {
                    System.out.print("Enter Doctor Name: ");
                    String dname = sc.nextLine();
                    System.out.print("Enter Specialization: ");
                    String spec = sc.nextLine();
                    hs.addDoctor(dname, spec);
                }
                case 3 -> {
                    System.out.print("Enter Patient ID: ");
                    String pid = sc.nextLine();
                    System.out.print("Enter Doctor ID: ");
                    String did = sc.nextLine();
                    System.out.print("Enter Date (DD-MM-YYYY): ");
                    String date = sc.nextLine();
                    hs.bookAppointment(pid, did, date);
                }
                case 4 -> hs.viewAllPatients();
                case 5 -> hs.viewAllDoctors();
                case 6 -> hs.viewAllAppointments();
                case 0 -> System.out.println("👋 Exiting...");
                default -> System.out.println("❌ Invalid choice!");
            }

        } while (choice != 0);
    }
}
