import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;
import java.util.stream.IntStream;

public final class DiceRollBenchmark {
    private static final int DEFAULT_N = 60_000_000;

    private DiceRollBenchmark() {
    }

    public static List<Integer> original() {
        return original(DEFAULT_N);
    }

    public static List<Integer> original(int n) {
        Random random = new Random();
        List<Integer> rolls = new ArrayList<>(n);

        for (int i = 0; i < n; i++) {
            rolls.add(random.nextInt(1, 7));
        }

        return rolls;
    }

    public static byte[] tuned() {
        return tuned(DEFAULT_N);
    }

    public static byte[] tuned(int n) {
        byte[] rolls = new byte[n];

        IntStream.range(0, n)
                .parallel()
                .forEach(i -> rolls[i] = (byte) ThreadLocalRandom.current().nextInt(1, 7));

        return rolls;
    }

    public static void profile() {
        profile(DEFAULT_N);
    }

    public static void profile(int n) {
        tuned(1);

        long t0 = System.nanoTime();
        original(n);
        long t1 = System.nanoTime();

        long t2 = System.nanoTime();
        tuned(n);
        long t3 = System.nanoTime();

        double originalTime = (t1 - t0) / 1_000_000_000.0;
        double tunedTime = (t3 - t2) / 1_000_000_000.0;

        System.out.printf("original: %.6f seconds%n", originalTime);
        System.out.printf("tuned:    %.6f seconds%n", tunedTime);
        System.out.printf("speedup:  %.2fx%n", originalTime / tunedTime);
    }

    public static void main(String[] args) {
        int n = args.length > 0 ? Integer.parseInt(args[0]) : DEFAULT_N;
        profile(n);
    }
}