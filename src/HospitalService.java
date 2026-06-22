import java.util.ArrayList;
import java.util.List;

public class HospitalService {
    private List<Patient> patients = new ArrayList<>();
    private List<Doctor> doctors = new ArrayList<>();
    private List<Appointment> appointments = new ArrayList<>();

    public void addPatient(String name, int age, String disease) {
        String id = IDGenerator.generatePatientId();
        Patient p = new Patient(id, name, age, disease);
        patients.add(p);
        System.out.println("✅ Patient added: " + p);
    }

    public void addDoctor(String name, String specialization) {
        String id = IDGenerator.generateDoctorId();
        Doctor d = new Doctor(id, name, specialization);
        doctors.add(d);
        System.out.println("✅ Doctor added: " + d);
    }

    public void bookAppointment(String patientId, String doctorId, String date) {
        Patient p = findPatientById(patientId);
        Doctor d = findDoctorById(doctorId);

        if (p != null && d != null) {
            String id = IDGenerator.generateAppointmentId();
            Appointment a = new Appointment(id, p, d, date);
            appointments.add(a);
            System.out.println("✅ Appointment booked:\n" + a);
        } else {
            System.out.println("❌ Invalid Patient or Doctor ID!");
        }
    }

    public void viewAllPatients() {
        System.out.println("\n📋 Patients List:");
        for (Patient p : patients) System.out.println(p);
    }

    public void viewAllDoctors() {
        System.out.println("\n📋 Doctors List:");
        for (Doctor d : doctors) System.out.println(d);
    }

    public void viewAllAppointments() {
        System.out.println("\n📋 Appointments:");
        for (Appointment a : appointments) System.out.println(a + "\n");
    }

    private Patient findPatientById(String id) {
        for (Patient p : patients) {
            if (p.getPatientId().equals(id)) return p;
        }
        return null;
    }

    private Doctor findDoctorById(String id) {
        for (Doctor d : doctors) {
            if (d.getDoctorId().equals(id)) return d;
        }
        return null;
    }
}
