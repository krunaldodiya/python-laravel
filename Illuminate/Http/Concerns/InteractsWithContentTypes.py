from Illuminate.Support.Str import Str


class InteractsWithContentTypes:
    def is_json(self):
        content_type = (
            self.header("Content-Type") if self.header("Content-Type") else ""
        )

        return Str.contains(content_type, ["/json", "+json"])
