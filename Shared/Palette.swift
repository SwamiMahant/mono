import Foundation

/// Monochrome palette for a modern professional look, as 0xRRGGBB.
public enum Palette {
    public static let berry1: UInt32 = 0xC7C7C7  // light gray
    public static let berry2: UInt32 = 0x949494
    public static let berry3: UInt32 = 0x616161
    public static let berry4: UInt32 = 0x383838  // deep charcoal
    public static let nose: UInt32 = 0x242424
    public static let ink: UInt32 = 0x171717
    public static let inkSoft: UInt32 = 0xBABABA
    public static let panel: UInt32 = 0x1F1F1F

    public static let gradient: [UInt32] = [berry1, berry2, berry3, berry4]
    public static let gradientStops: [Double] = [0, 0.34, 0.68, 1]

    public static func rgb(_ hex: UInt32) -> (r: Double, g: Double, b: Double) {
        (Double((hex >> 16) & 0xFF) / 255, Double((hex >> 8) & 0xFF) / 255, Double(hex & 0xFF) / 255)
    }
}
