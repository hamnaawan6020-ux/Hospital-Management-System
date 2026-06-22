public class IDGenerator {
    private static int patientCounter = 1000;
    private static int doctorCounter = 2000;
    private static int appointmentCounter = 3000;

    public static String generatePatientId() {
        return "P" + (++patientCounter);
    }

    public static String generateDoctorId() {
        return "D" + (++doctorCounter);
    }

    public static String generateAppointmentId() {
        return "A" + (++appointmentCounter);
    }
}
