#include <drogon/drogon.h>
#include <thread>
#include <chrono>
#include <future>
#include <cstdlib>

using namespace drogon;


int main(){
    trantor::Logger::setLogLevel(trantor::Logger::kTrace);
    {
        int count = 0;
        auto client = HttpClient::newHttpClient("http://www.baidu.com");
        auto req = HttpRequest::newHttpRequest();
        req->setMethod(drogon::Get);
        req->setPath("/s");
        req->setParameter("wd", "wx");
        req->setParameter("oq", "wx");

        for (int i = 0; i < 10; ++i)
        {
            client->sendRequest(
                req,
                [&count](ReqResult result, const HttpResponsePtr &response) {
                    std::cout << "receive response!" << std::endl;
                    // auto headers=response.
                    ++count;
                    std::cout << response->getBody() << std::endl;
                    auto cookies = response->cookies();
                    for (auto const &cookie : cookies)
                    {
                        std::cout << cookie.first << "="
                                  << cookie.second.value()
                                  << ":domain=" << cookie.second.domain()
                                  << std::endl;
                    }
                    std::cout << "count=" << count << std::endl;
                });
        }
    }

    app().run();
}

int maini()
{
    app().setLogPath("./")
         .setLogLevel(trantor::Logger::kInfo)
         .addListener("0.0.0.0", 80123)
         .setThreadNum(2)
         .enableRunAsDaemon()
         .run();

    using namespace std::chrono_literals;
    std::cout << "Hello drogon!" << std::endl;
    std::this_thread::sleep_for(2s);
    std::cout << "bye" << std::endl;
    exit(-1);
}
