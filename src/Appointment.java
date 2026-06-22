public class Appointment {
    private String appointmentId;
    private Patient patient;
    private Doctor doctor;
    private String date;

    public Appointment(String appointmentId, Patient patient, Doctor doctor, String date) {
        this.appointmentId = appointmentId;
        this.patient = patient;
        this.doctor = doctor;
        this.date = date;
    }

    @Override
    public String toString() {
        return "Appointment ID: " + appointmentId + "\n"
                + "Patient: " + patient.getName() + " (" + patient.getPatientId() + ")\n"
                + "Doctor: " + doctor.getName() + " (" + doctor.getDoctorId() + ")\n"
                + "Date: " + date;
    }
}
