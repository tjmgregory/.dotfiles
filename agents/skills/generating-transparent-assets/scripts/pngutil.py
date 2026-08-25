"""Pure-python PNG decode/encode (8-bit RGB/RGBA). No PIL needed."""
import struct, zlib


def decode_png(path):
    """Returns (w, h, channels, bytearray of pixels)."""
    d = open(path, "rb").read()
    assert d[:8] == b"\x89PNG\r\n\x1a\n", f"{path}: not a PNG"
    w, h, bit, ctype = struct.unpack(">IIBB", d[16:26])
    assert bit == 8 and ctype in (2, 6), f"{path}: unsupported bit={bit} ctype={ctype} (need 8-bit RGB/RGBA)"
    bpp = 3 if ctype == 2 else 4
    idat = b""
    i = 8
    while i < len(d):
        ln = struct.unpack(">I", d[i:i + 4])[0]
        typ = d[i + 4:i + 8]
        if typ == b"IDAT":
            idat += d[i + 8:i + 8 + ln]
        i += 12 + ln
    raw = zlib.decompress(idat)
    stride = w * bpp
    out = bytearray(w * h * bpp)
    prev = bytearray(stride)
    pos = 0
    for y in range(h):
        f = raw[pos]
        pos += 1
        row = bytearray(raw[pos:pos + stride])
        pos += stride
        if f == 1:
            for x in range(bpp, stride):
                row[x] = (row[x] + row[x - bpp]) & 0xFF
        elif f == 2:
            for x in range(stride):
                row[x] = (row[x] + prev[x]) & 0xFF
        elif f == 3:
            for x in range(stride):
                a = row[x - bpp] if x >= bpp else 0
                row[x] = (row[x] + ((a + prev[x]) >> 1)) & 0xFF
        elif f == 4:
            for x in range(stride):
                a = row[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                row[x] = (row[x] + pr) & 0xFF
        out[y * stride:(y + 1) * stride] = row
        prev = row
    return w, h, bpp, out


def encode_png(path, w, h, bpp, pix):
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    ctype = 2 if bpp == 3 else 6
    raw = bytearray()
    stride = w * bpp
    for y in range(h):
        raw.append(0)
        raw += pix[y * stride:(y + 1) * stride]
    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, ctype, 0, 0, 0))
    out += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    out += chunk(b"IEND", b"")
    open(path, "wb").write(out)


def has_real_alpha(path):
    """True only if PNG has an alpha channel with at least one non-opaque pixel."""
    w, h, bpp, px = decode_png(path)
    if bpp != 4:
        return False
    return any(px[i * 4 + 3] != 255 for i in range(w * h))
