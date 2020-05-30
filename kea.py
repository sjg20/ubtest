import tbot
from tbot.machine import connector, linux


class ArmV7Toolchain(linux.build.Toolchain):
    def enable(self, host):
        # Set all environment variables to "enable" this toolchain
        prefix = "~/.buildman-toolchains/gcc-7.3.0-nolibc/arm-linux-gnueabi/bin/arm-linux-gnueabi-"
        host.env("CROSS_COMPILE", prefix)
        #host.env("ARCH", "arm")

        for tool in [
            "gcc", "objdump", "size", "ar", "nm", "strings",
            "as", "ld", "objcopy", "readelf", "strip",
        ]:
            host.env(tool.upper(), prefix + tool)

        # Optionally set CFLAGS and LDFLAGS
        # host.env("CFLAGS", "...")
        # host.env("LDFLAGS", "...")

class Aarch64Toolchain(linux.build.Toolchain):
    def enable(self, host):
        # Set all environment variables to "enable" this toolchain
        prefix = "~/.buildman-toolchains/gcc-7.3.0-nolibc/aarch64-linux/bin/aarch64-linux-"
        host.env("CROSS_COMPILE", prefix)
        #host.env("ARCH", "arm")

        for tool in [
            "gcc", "objdump", "size", "ar", "nm", "strings",
            "as", "ld", "objcopy", "readelf", "strip",
        ]:
            host.env(tool.upper(), prefix + tool)

        # Optionally set CFLAGS and LDFLAGS
        # host.env("CFLAGS", "...")
        # host.env("LDFLAGS", "...")


class I386Toolchain(linux.build.Toolchain):
    def enable(self, host):
        # Set all environment variables to "enable" this toolchain
        prefix = "~/.buildman-toolchains/gcc-7.3.0-nolibc/i386-linux/bin/i386-linux-"
        host.env("CROSS_COMPILE", prefix)

        for tool in [
            "gcc", "objdump", "size", "ar", "nm", "strings",
            "as", "ld", "objcopy", "readelf", "strip",
        ]:
            host.env(tool.upper(), prefix + tool)

        # Optionally set CFLAGS and LDFLAGS
        host.env("BUILD_ROM", "1")
        # host.env("LDFLAGS", "...")


class KeaLab(
    connector.ParamikoConnector,
    linux.Bash,
    linux.Lab,
    linux.Builder,
):
    name = "sglass"
    hostname = "kea"

    @property
    def workdir(self):
        return linux.Workdir.athome(self, "tbot-workdir")

    @property
    def toolchains(self):
        # Should return a dict of all toolchains available on this host.  Each
        # toolchain is identified by a (unique) string.  For pcduino3 in this
        # example, a toolchain named `armv7-a` is defined.
        return {
            "armv7-a": ArmV7Toolchain(),
            "aarch64": Aarch64Toolchain(),
            "i386": I386Toolchain(),
        }

    def build(self):
        # Kea is also used as the build-host so just return (a cloned) self
        return self.clone()


# tbot will check for `LAB`, don't forget to set it!
LAB = KeaLab
